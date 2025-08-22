import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Any, Optional

def analyze_csv(file_path: str) -> Optional[Dict[str, Any]]:
    """Analyze CSV file and return comprehensive statistics and insights."""
    try:
        # Read CSV file
        df = pd.read_csv(file_path)
        
        if df.empty:
            logging.error("CSV file is empty")
            return None
        
        # Basic info
        row_count, column_count = df.shape
        
        # Analyze columns
        columns_info = {}
        stats = {}
        
        for column in df.columns:
            col_info = {
                'name': str(column),
                'type': str(df[column].dtype),
                'non_null_count': int(df[column].count()),
                'null_count': int(df[column].isnull().sum()),
                'unique_count': int(df[column].nunique())
            }
            
            # Determine if column is numeric
            if pd.api.types.is_numeric_dtype(df[column]):
                col_info['is_numeric'] = True
                # Check if all values are null
                all_null = df[column].isnull().all()
                col_stats = {
                    'mean': float(round(df[column].mean(), 2)) if not all_null and not pd.isna(df[column].mean()) else None,
                    'median': float(round(df[column].median(), 2)) if not all_null and not pd.isna(df[column].median()) else None,
                    'std': float(round(df[column].std(), 2)) if not all_null and not pd.isna(df[column].std()) else None,
                    'min': float(round(df[column].min(), 2)) if not all_null and not pd.isna(df[column].min()) else None,
                    'max': float(round(df[column].max(), 2)) if not all_null and not pd.isna(df[column].max()) else None,
                    'q25': float(round(df[column].quantile(0.25), 2)) if not all_null and not pd.isna(df[column].quantile(0.25)) else None,
                    'q75': float(round(df[column].quantile(0.75), 2)) if not all_null and not pd.isna(df[column].quantile(0.75)) else None
                }
                col_info.update(col_stats)
                stats[column] = col_stats
            else:
                col_info['is_numeric'] = False
                # For categorical data, get value counts
                value_counts = df[column].value_counts().head(10)
                # Convert to regular Python types
                top_values_dict = {str(k): int(v) for k, v in value_counts.items()}
                col_info['top_values'] = top_values_dict
                stats[column] = {
                    'top_values': top_values_dict,
                    'most_common': str(value_counts.index[0]) if len(value_counts) > 0 else None
                }
            
            columns_info[column] = col_info
        
        return {
            'row_count': int(row_count),
            'column_count': int(column_count),
            'columns_info': columns_info,
            'stats': stats,
            'memory_usage': f"{float(df.memory_usage(deep=True).sum()) / 1024:.1f} KB"
        }
        
    except Exception as e:
        logging.error(f"Error analyzing CSV: {str(e)}")
        return None

def get_column_chart_data(file_path: str, column: str) -> Dict[str, Any]:
    """Get chart data for a specific column."""
    try:
        df = pd.read_csv(file_path)
        
        if column not in df.columns:
            return {'error': 'Column not found'}
        
        col_data = df[column].dropna()
        
        if pd.api.types.is_numeric_dtype(col_data):
            # For numeric data, create histogram
            hist_data, bin_edges = np.histogram(col_data, bins=20)
            labels = [f"{bin_edges[i]:.1f}-{bin_edges[i+1]:.1f}" for i in range(len(hist_data))]
            
            return {
                'type': 'histogram',
                'labels': [str(label) for label in labels],
                'data': [int(x) for x in hist_data.tolist()],
                'title': f'Distribution of {column}'
            }
        else:
            # For categorical data, create bar chart
            value_counts = col_data.value_counts().head(15)
            
            return {
                'type': 'bar',
                'labels': [str(x) for x in value_counts.index.tolist()],
                'data': [int(x) for x in value_counts.values.tolist()],
                'title': f'Top Values in {column}'
            }
            
    except Exception as e:
        logging.error(f"Error getting chart data: {str(e)}")
        return {'error': 'Failed to generate chart data'}

def get_insights(file_path: str) -> List[str]:
    """Generate insights about the dataset."""
    try:
        df = pd.read_csv(file_path)
        insights = []
        
        # Dataset size insight
        insights.append(f"Dataset contains {len(df):,} rows and {len(df.columns)} columns")
        
        # Missing data insights
        missing_percent = (df.isnull().sum() / len(df) * 100).round(1)
        high_missing = missing_percent[missing_percent > 50]
        if len(high_missing) > 0:
            insights.append(f"High missing data in: {', '.join([str(x) for x in high_missing.index.tolist()])}")
        
        # Numeric columns insights
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            insights.append(f"Found {len(numeric_cols)} numeric columns for statistical analysis")
        
        # Categorical columns insights
        cat_cols = df.select_dtypes(exclude=[np.number]).columns
        if len(cat_cols) > 0:
            insights.append(f"Found {len(cat_cols)} categorical columns")
        
        # Duplicate rows
        duplicates = int(df.duplicated().sum())
        if duplicates > 0:
            insights.append(f"Found {duplicates} duplicate rows ({duplicates/len(df)*100:.1f}%)")
        
        return insights[:5]  # Return top 5 insights
        
    except Exception as e:
        logging.error(f"Error generating insights: {str(e)}")
        return ["Unable to generate insights for this dataset"]
