# Career & Data Insights Platform

A full-stack Flask web application that provides AI-powered resume analysis and interactive data exploration with multi-language support (English, Russian, Georgian).

## Features

### 🎯 AI-Powered Resume Analyzer
- Upload PDF/DOCX resumes for comprehensive analysis
- Multi-language support (English, Russian, Georgian)
- ATS compatibility scoring with visual indicators
- Skills extraction (technical and soft skills)
- Career improvement suggestions
- Downloadable PDF reports
- Professional visualizations with Chart.js

### 📊 Interactive Data Explorer
- CSV file analysis with statistical summaries
- Dynamic chart generation for any column
- Beautiful multi-color visualizations
- Automatic data type detection (numeric vs categorical)
- Interactive tooltips and animations
- Responsive design for all devices

### 🔐 User Authentication
- Secure user registration and login
- Profile management with analysis history
- Session-based authentication
- PostgreSQL database integration

### 🎨 Modern Design
- TailwindCSS for responsive styling
- Professional gradient themes
- Smooth animations and transitions
- Mobile-first responsive design
- Font Awesome icons

## Technology Stack

- **Backend**: Flask, SQLAlchemy, PostgreSQL
- **Frontend**: HTML5, TailwindCSS, JavaScript, Chart.js
- **File Processing**: PyPDF2, python-docx, pandas, numpy
- **Authentication**: Flask-Login, Werkzeug
- **Visualizations**: Chart.js with custom color palettes
- **Language Detection**: Custom language detector
- **Report Generation**: ReportLab for PDF exports

## Installation & Setup

### Prerequisites
- Python 3.11+
- PostgreSQL database
- pip package manager

### 1. Install Dependencies

#### Option A: Using requirements file
```bash
pip install -r render-requirements.txt
```

#### Option B: Manual installation
```bash
pip install flask flask-sqlalchemy flask-login flask-migrate gunicorn
pip install pandas pypdf2 python-docx reportlab wordcloud spacy nltk
pip install matplotlib seaborn plotly pillow psycopg2-binary
pip install bcrypt email-validator langdetect scikit-learn
```

### 2. Environment Variables
Create a `.env` file or set these environment variables:
```bash
DATABASE_URL=postgresql://username:password@localhost/database_name
SESSION_SECRET=your-secret-key-here
FLASK_SECRET_KEY=your-flask-secret-key
```

### 3. Database Setup
```bash
# Initialize database
python -c "from app import app, db; app.app_context().push(); db.create_all()"

# Or use Flask-Migrate (recommended)
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 4. Run the Application

#### Development Mode
```bash
python main.py
```

#### Production Mode (with Gunicorn)
```bash
gunicorn --bind 0.0.0.0:5000 --reuse-port --reload main:app
```

### 5. Access the Application
Open your browser and navigate to:
- Local: `http://localhost:5000`
- Network: `http://0.0.0.0:5000`

## Project Structure

```
career-insights-platform/
├── app.py                 # Flask application factory
├── main.py               # Application entry point
├── routes.py             # Main application routes
├── auth.py               # Authentication routes
├── models.py             # Database models
├── services/
│   ├── ats_engine.py     # Resume analysis engine
│   ├── csv_analyzer.py   # CSV data analysis
│   ├── language_detector.py # Multi-language detection
│   └── pdf_generator.py  # Report generation
├── templates/
│   ├── base.html         # Base template
│   ├── index.html        # Landing page
│   ├── resume_analyzer.html
│   ├── data_explorer.html
│   ├── results.html      # Analysis results
│   └── auth/             # Authentication templates
├── static/               # Static assets
├── uploads/              # File upload directory
└── requirements.txt      # Python dependencies
```

## Usage

### Resume Analysis
1. Navigate to "Resume Analyzer"
2. Upload a PDF or DOCX resume
3. View comprehensive analysis including:
   - ATS compatibility score
   - Extracted skills (technical & soft)
   - Missing keywords
   - Career improvement suggestions
4. Download detailed PDF report

### Data Exploration
1. Navigate to "Data Explorer"
2. Upload a CSV file
3. View dataset overview and statistics
4. Select any column to generate interactive visualizations
5. Explore different chart types based on data types

### User Features
- Create account for analysis history
- View all past analyses in profile
- Secure session management
- Multi-language interface support

## API Endpoints

- `GET /` - Landing page
- `GET /resume-analyzer` - Resume upload form
- `POST /upload-resume` - Process resume upload
- `GET /data-explorer` - CSV upload form
- `POST /upload-csv` - Process CSV upload
- `GET /resume-results/<id>` - View resume analysis
- `GET /csv-results/<id>` - View CSV analysis
- `GET /api/chart-data/<upload_id>/<column>` - Get chart data
- `GET /download-report/<id>` - Download PDF report
- `GET /auth/login` - User login
- `POST /auth/register` - User registration
- `GET /auth/profile` - User profile

## Configuration

### Database Configuration
The application supports both SQLite (development) and PostgreSQL (production):
```python
# Development
SQLALCHEMY_DATABASE_URI = "sqlite:///app.db"

# Production
SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
```

### Upload Configuration
```python
UPLOAD_FOLDER = "uploads/"
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
```

### Supported File Types
- **Resumes**: PDF, DOCX
- **Data**: CSV files
- **Languages**: English, Russian, Georgian

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Ensure PostgreSQL is running
   - Check DATABASE_URL environment variable
   - Verify database credentials

2. **File Upload Issues**
   - Check file size (max 16MB)
   - Ensure uploads/ directory exists
   - Verify file permissions

3. **Chart Loading Problems**
   - Check browser console for errors
   - Ensure Chart.js is loaded
   - Verify API endpoints are accessible

4. **Language Detection Issues**
   - Ensure text content is sufficient
   - Check supported languages list
   - Verify encoding compatibility

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## 🚀 Render.com Deployment

### Quick Deploy to Render

1. **Create Render Account** at [render.com](https://render.com)

2. **Connect GitHub Repository** (after uploading your project to GitHub)

3. **Create Web Service** with these settings:
   - **Build Command:** `pip install -r render-requirements.txt`
   - **Start Command:** `gunicorn --bind 0.0.0.0:$PORT main:app`
   - **Environment:** `Python 3.11`

4. **Environment Variables** (in Render dashboard):
   ```
   DATABASE_URL=<your-postgresql-database-url>
   SESSION_SECRET=<random-secret-key>
   FLASK_SECRET_KEY=<random-secret-key>
   PYTHON_VERSION=3.11.0
   ```

5. **Database Setup:**
   - Create PostgreSQL database in Render
   - Copy the Internal Database URL to `DATABASE_URL`
   - Database tables will be created automatically on first run

### Render-Specific Files

- **`render-requirements.txt`** - All Python dependencies with versions
- **Port Configuration** - Automatically handled by `$PORT` environment variable
- **Database** - PostgreSQL recommended for production

### Alternative: One-Click Deploy

You can also deploy directly from GitHub:

1. Fork/upload project to GitHub
2. Connect to Render
3. Deploy automatically

### Production Notes

- Uses PostgreSQL instead of SQLite
- Handles file uploads in memory (Render filesystem is ephemeral)
- Automatically scales based on traffic
- SSL certificates included free
- Custom domain support available

## Support

For support and questions:
- Check the troubleshooting section
- Review the project documentation
- Create an issue in the repository

---

**Built with ❤️ using Flask and modern web technologies**