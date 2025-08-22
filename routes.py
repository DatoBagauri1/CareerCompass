import os
import json
import uuid
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app, send_file
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from services.parser import extract_text_from_file
from services.ats_engine import analyze_resume
from services.csv_analyzer import analyze_csv
from services.report_generator import generate_pdf_report
from services.language_detector import detect_language
from models import Resume, Analysis, CSVUpload
from app import db

main_bp = Blueprint('main', __name__)

ALLOWED_RESUME_EXTENSIONS = {'pdf', 'docx'}
ALLOWED_CSV_EXTENSIONS = {'csv'}

def allowed_file(filename, allowed_extensions):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/resume-analyzer')
def resume_analyzer():
    return render_template('resume_analyzer.html')

@main_bp.route('/data-explorer')
def data_explorer():
    return render_template('data_explorer.html')

@main_bp.route('/upload-resume', methods=['POST'])
def upload_resume():
    try:
        if 'resume_file' not in request.files:
            flash('No file selected', 'error')
            return redirect(url_for('main.resume_analyzer'))
        
        file = request.files['resume_file']
        job_description = request.form.get('job_description', '').strip()
        
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(url_for('main.resume_analyzer'))
        
        if file and file.filename and allowed_file(file.filename, ALLOWED_RESUME_EXTENSIONS):
            # Generate unique filename
            file_ext = file.filename.rsplit('.', 1)[1].lower()
            unique_filename = f"{uuid.uuid4()}.{file_ext}"
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
            
            # Save file
            file.save(file_path)
            
            # Extract text
            text_content = extract_text_from_file(file_path)
            
            if not text_content.strip():
                flash('Could not extract text from the file. Please ensure it contains readable text.', 'error')
                os.remove(file_path)
                return redirect(url_for('main.resume_analyzer'))
            
            # Detect language
            detected_language = detect_language(text_content)
            
            # Save to database
            resume = Resume(
                user_id=current_user.id if current_user and current_user.is_authenticated else None,
                filename=unique_filename,
                original_filename=file.filename,
                file_type=file_ext,
                text_content=text_content,
                language=detected_language
            )
            db.session.add(resume)
            db.session.commit()
            
            # Analyze resume with language support
            analysis_result = analyze_resume(text_content, job_description, detected_language)
            
            # Ensure data is JSON serializable
            try:
                skills_json = json.dumps(analysis_result.get('skills', {}))
                missing_keywords_json = json.dumps(analysis_result.get('missing_keywords', []))
                suggestions_json = json.dumps(analysis_result.get('suggestions', []))
            except (TypeError, ValueError) as e:
                current_app.logger.error(f"JSON serialization error: {str(e)}")
                # Fallback to string representations
                skills_json = json.dumps({})
                missing_keywords_json = json.dumps([])
                suggestions_json = json.dumps([])
            
            # Save analysis
            analysis = Analysis(
                resume_id=resume.id,
                job_description=job_description,
                ats_score=float(analysis_result.get('ats_score', 0)),
                extracted_skills=skills_json,
                missing_keywords=missing_keywords_json,
                suggestions=suggestions_json
            )
            db.session.add(analysis)
            db.session.commit()
            
            return redirect(url_for('main.resume_results', analysis_id=analysis.id))
        
        else:
            flash('Invalid file type. Please upload PDF or DOCX files only.', 'error')
            return redirect(url_for('main.resume_analyzer'))
            
    except Exception as e:
        current_app.logger.error(f"Error processing resume: {str(e)}")
        flash('An error occurred while processing your resume. Please try again.', 'error')
        return redirect(url_for('main.resume_analyzer'))

@main_bp.route('/upload-csv', methods=['POST'])
def upload_csv():
    try:
        if 'csv_file' not in request.files:
            flash('No file selected', 'error')
            return redirect(url_for('main.data_explorer'))
        
        file = request.files['csv_file']
        
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(url_for('main.data_explorer'))
        
        if file and allowed_file(file.filename, ALLOWED_CSV_EXTENSIONS):
            # Generate unique filename
            unique_filename = f"{uuid.uuid4()}.csv"
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
            
            # Save file
            file.save(file_path)
            
            # Analyze CSV
            analysis_result = analyze_csv(file_path)
            
            if analysis_result is None:
                flash('Error analyzing CSV file. Please ensure it\'s a valid CSV with proper formatting.', 'error')
                os.remove(file_path)
                return redirect(url_for('main.data_explorer'))
            
            # Save to database
            csv_upload = CSVUpload(
                user_id=current_user.id if current_user and current_user.is_authenticated else None,
                filename=unique_filename,
                original_filename=file.filename,
                columns_info=json.dumps(analysis_result['columns_info']),
                stats_summary=json.dumps(analysis_result['stats']),
                row_count=analysis_result['row_count'],
                column_count=analysis_result['column_count']
            )
            db.session.add(csv_upload)
            db.session.commit()
            
            return redirect(url_for('main.csv_results', upload_id=csv_upload.id))
        
        else:
            flash('Invalid file type. Please upload CSV files only.', 'error')
            return redirect(url_for('main.data_explorer'))
            
    except Exception as e:
        current_app.logger.error(f"Error processing CSV: {str(e)}")
        flash('An error occurred while processing your CSV file. Please try again.', 'error')
        return redirect(url_for('main.data_explorer'))

@main_bp.route('/resume-results/<int:analysis_id>')
def resume_results(analysis_id):
    analysis = Analysis.query.get_or_404(analysis_id)
    
    # Parse JSON fields
    skills = json.loads(analysis.extracted_skills) if analysis.extracted_skills else []
    missing_keywords = json.loads(analysis.missing_keywords) if analysis.missing_keywords else []
    suggestions = json.loads(analysis.suggestions) if analysis.suggestions else []
    
    return render_template('results.html', 
                         analysis=analysis,
                         skills=skills,
                         missing_keywords=missing_keywords,
                         suggestions=suggestions,
                         result_type='resume')

@main_bp.route('/csv-results/<int:upload_id>')
def csv_results(upload_id):
    csv_upload = CSVUpload.query.get_or_404(upload_id)
    
    # Parse JSON fields
    columns_info = json.loads(csv_upload.columns_info) if csv_upload.columns_info else {}
    stats = json.loads(csv_upload.stats_summary) if csv_upload.stats_summary else {}
    
    return render_template('results.html', 
                         csv_upload=csv_upload,
                         columns_info=columns_info,
                         stats=stats,
                         result_type='csv')

@main_bp.route('/download-report/<int:analysis_id>')
def download_report(analysis_id):
    try:
        analysis = Analysis.query.get_or_404(analysis_id)
        
        # Generate PDF report
        report_path = generate_pdf_report(analysis)
        
        if report_path and os.path.exists(report_path):
            return send_file(report_path, as_attachment=True, 
                           download_name=f"resume_analysis_report_{analysis_id}.pdf")
        else:
            flash('Error generating report. Please try again.', 'error')
            return redirect(url_for('main.resume_results', analysis_id=analysis_id))
            
    except Exception as e:
        current_app.logger.error(f"Error generating report: {str(e)}")
        flash('Error generating report. Please try again.', 'error')
        return redirect(url_for('main.resume_results', analysis_id=analysis_id))

@main_bp.route('/api/chart-data/<int:upload_id>/<column>')
def get_chart_data(upload_id, column):
    try:
        csv_upload = CSVUpload.query.get_or_404(upload_id)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], csv_upload.filename)
        
        from services.csv_analyzer import get_column_chart_data
        chart_data = get_column_chart_data(file_path, column)
        
        return jsonify(chart_data)
        
    except Exception as e:
        current_app.logger.error(f"Error getting chart data: {str(e)}")
        return jsonify({'error': 'Failed to generate chart data'}), 500
