# LC Index - Document Management System

A comprehensive document management and processing system with enhanced Excel processing capabilities, user level access controls, and multi-document type support.

## Features

### 1. Document Type Selection
- **Excel Processing**: Process Excel files with configurable headers
- **Pro forma Invoice**: Generate proforma invoices with PI Number and PI Date
- **LC Document**: Letter of Credit processing with LC Number and LC Date
- **Packing List**: Generate packing lists with Commercial Invoice details
- **Commercial Invoice**: Create commercial invoices with comprehensive fields
- **Value Sheet**: Generate value sheets with LC and Bill of Entry details
- **Loading List**: Create loading lists with shipping and container information

### 2. Enhanced Excel Processing
- **No JSON Input Option**: Removed as per requirements
- **Excel Format**: No prefix headers required
- **Header Configuration**: 
  - Show all headers for specification
  - Configure headers to keep, sum, subtotal, or grand total
  - Insert new headers with various sources:
    - Text input
    - Auto numbering with custom format
    - Calculations with multiple headers
    - Menu lists from attached sheets
- **Action Buttons**: Add action buttons to headers or rows (Check list, Edit, Apply, Delete)

### 3. Tabbed Interface
- **Create Document Tab**: Main document creation and processing interface
- **Document Types Tab**: Manage and configure document types with fields and databases
- **User Management Tab**: Available for Admin and Developer levels

### 4. User Level Access Controls
- **User Level**: Basic document creation and processing
- **Admin Level**: Document type management, user administration, system configuration
- **Developer Level**: Database management, API configuration, system logs, custom integrations

### 5. Action Buttons
- **Save**: Save documents under selected document type
- **Preview**: Show processed data in tabular format
- **Edit**: Edit processed documents
- **Delete**: Delete processed documents

## Installation

1. **Clone or download the project to the LC index folder**:
   ```bash
   # Files should be in: C:\Users\USER\Desktop\LC index
   # Or in Linux: /home/ubuntu/LC_index
   ```

2. **Install required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python main.py
   ```

4. **Access the application**:
   - Local: http://localhost:5000
   - The application will be available on all network interfaces (0.0.0.0)

## Project Structure

```
LC_index/
├── main.py                 # Main Flask application
├── requirements.txt        # Python dependencies
├── README.md              # This documentation
├── data_structure.py      # Data structure definitions
├── src/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py        # User and database models
│   └── routes/
│       ├── __init__.py
│       ├── user.py        # User management routes
│       └── sheets.py      # Document processing routes
├── static/
│   └── index.html         # Frontend interface
├── database/
│   └── app.db            # SQLite database (auto-created)
└── test_app.py           # Application testing script
```

## API Endpoints

### Document Processing
- `POST /api/sheets/upload` - Upload and process Excel files
- `POST /api/sheets/process` - Process JSON data
- `GET /api/sheets/headers` - Extract headers from Excel files
- `GET /api/sheets/sample` - Get sample data

### Document Types
- `POST /api/sheets/documents/proforma` - Process Pro forma Invoice
- `POST /api/sheets/documents/lc` - Process LC Document
- `POST /api/sheets/documents/packing` - Process Packing List
- `POST /api/sheets/documents/commercial` - Process Commercial Invoice
- `POST /api/sheets/documents/value` - Process Value Sheet
- `POST /api/sheets/documents/loading` - Process Loading List

### User Management
- `POST /api/register` - Register new user
- `POST /api/login` - User login
- `POST /api/logout` - User logout
- `GET /api/profile` - Get user profile
- `PUT /api/profile` - Update user profile
- `GET /api/users` - Get all users (Admin only)
- `PUT /api/users/<id>` - Update user (Admin only)
- `DELETE /api/users/<id>` - Delete user (Admin only)

### System
- `GET /health` - Health check
- `GET /api/info` - API information

## Usage

### 1. Document Creation
1. Select document type from the grid
2. For Excel processing:
   - Upload Excel file
   - Configure headers as needed
   - Process the document
3. For other document types:
   - Fill in required fields
   - Process the document

### 2. Header Configuration (Excel Processing)
- **Keep**: Maintain header in output
- **Sum**: Calculate sum for numeric columns
- **Subtotal**: Generate subtotals by groups
- **Grand Total**: Calculate grand totals
- **Edit**: Modify header name
- **Delete**: Remove header from processing

### 3. Document Management
- **Save**: Store processed documents
- **Preview**: View results in tabular format
- **Edit**: Modify document data
- **Delete**: Remove documents

### 4. User Level Management
- Switch between User, Admin, and Developer sections
- Access level-appropriate features
- Manage users and system configuration (Admin/Developer only)

## Document Types Configuration

Each document type includes:
- **Name**: Display name
- **Description**: Purpose description
- **Required Fields**: List of mandatory fields
- **Status**: Active/Inactive toggle
- **Actions**: Edit, Toggle status, Delete

### Predefined Document Types:
1. **Pro forma Invoice**: PI Number, PI Date
2. **LC Document**: LC Number, LC Date
3. **Packing List**: CI Number, CI Date, LC Number, B/L Number
4. **Commercial Invoice**: CI Number, CI Date, LC Number, B/L Number
5. **Value Sheet**: LC Number, B/E Number, B/E Date
6. **Loading List**: LC Number, Loading Date, Ports, Container details

## Security Features

- User authentication with session tokens
- Role-based access control (User/Admin/Developer)
- Password hashing
- Session management
- CORS enabled for frontend-backend communication

## Database Schema

### Users Table
- ID, Username, Email, Password Hash
- User Level, Active Status
- Created At, Last Login

### Document Types Table
- ID, Name, Description, Fields (JSON)
- Active Status, Created By, Created At

### Documents Table
- ID, Document Type ID, Name, Data (JSON)
- Created By, Created At, Updated At

### User Sessions Table
- ID, User ID, Session Token
- Expires At, Created At

## Development

### Testing
Run the test script to verify functionality:
```bash
python test_app.py
```

### Adding New Document Types
1. Use the Document Types tab interface
2. Or add via API endpoint
3. Configure required fields and validation

### Customization
- Modify `static/index.html` for frontend changes
- Update `src/routes/sheets.py` for processing logic
- Extend `src/models/user.py` for database schema changes

## Requirements

- Python 3.7+
- Flask 3.0.3
- Flask-SQLAlchemy 3.1.1
- Flask-CORS 6.0.1
- openpyxl 3.1.5
- Werkzeug 3.0.4

## License

This project is developed for internal use in the LC Index document management system.

## Support

For technical support or feature requests, contact the development team.

