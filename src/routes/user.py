from flask import Blueprint, request, jsonify, session
from src.models.user import db, User, UserSession
from datetime import datetime, timedelta
import secrets
import json

user_bp = Blueprint('user', __name__)

def require_auth(f):
    """Decorator to require authentication."""
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'error': 'Authentication required'}), 401
        
        try:
            token = auth_header.split(' ')[1]  # Bearer <token>
            user_session = UserSession.query.filter_by(session_token=token).first()
            
            if not user_session or user_session.is_expired():
                return jsonify({'error': 'Invalid or expired token'}), 401
            
            request.current_user = User.query.get(user_session.user_id)
            return f(*args, **kwargs)
        except:
            return jsonify({'error': 'Invalid token format'}), 401
    
    decorated_function.__name__ = f.__name__
    return decorated_function

def require_level(level):
    """Decorator to require specific user level."""
    def decorator(f):
        def decorated_function(*args, **kwargs):
            if not hasattr(request, 'current_user'):
                return jsonify({'error': 'Authentication required'}), 401
            
            user_levels = {'user': 1, 'admin': 2, 'developer': 3}
            required_level = user_levels.get(level, 1)
            current_level = user_levels.get(request.current_user.user_level, 1)
            
            if current_level < required_level:
                return jsonify({'error': 'Insufficient permissions'}), 403
            
            return f(*args, **kwargs)
        
        decorated_function.__name__ = f.__name__
        return decorated_function
    return decorator

@user_bp.route('/register', methods=['POST'])
def register():
    """Register a new user."""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['username', 'email', 'password']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Check if user already exists
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'Username already exists'}), 400
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already exists'}), 400
        
        # Create new user
        user = User(
            username=data['username'],
            email=data['email'],
            user_level=data.get('user_level', 'user')
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'message': 'User registered successfully',
            'user': user.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@user_bp.route('/login', methods=['POST'])
def login():
    """User login."""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('username') or not data.get('password'):
            return jsonify({'error': 'Username and password required'}), 400
        
        # Find user
        user = User.query.filter_by(username=data['username']).first()
        
        if not user or not user.check_password(data['password']):
            return jsonify({'error': 'Invalid username or password'}), 401
        
        if not user.active:
            return jsonify({'error': 'Account is deactivated'}), 401
        
        # Create session token
        session_token = secrets.token_urlsafe(32)
        expires_at = datetime.utcnow() + timedelta(hours=24)
        
        user_session = UserSession(
            user_id=user.id,
            session_token=session_token,
            expires_at=expires_at
        )
        
        # Update last login
        user.last_login = datetime.utcnow()
        
        db.session.add(user_session)
        db.session.commit()
        
        return jsonify({
            'message': 'Login successful',
            'token': session_token,
            'user': user.to_dict(),
            'expires_at': expires_at.isoformat()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@user_bp.route('/logout', methods=['POST'])
@require_auth
def logout():
    """User logout."""
    try:
        auth_header = request.headers.get('Authorization')
        token = auth_header.split(' ')[1]
        
        user_session = UserSession.query.filter_by(session_token=token).first()
        if user_session:
            db.session.delete(user_session)
            db.session.commit()
        
        return jsonify({'message': 'Logout successful'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@user_bp.route('/profile', methods=['GET'])
@require_auth
def get_profile():
    """Get current user profile."""
    return jsonify(request.current_user.to_dict())

@user_bp.route('/profile', methods=['PUT'])
@require_auth
def update_profile():
    """Update current user profile."""
    try:
        data = request.get_json()
        user = request.current_user
        
        # Update allowed fields
        if 'email' in data:
            # Check if email is already taken by another user
            existing_user = User.query.filter_by(email=data['email']).first()
            if existing_user and existing_user.id != user.id:
                return jsonify({'error': 'Email already exists'}), 400
            user.email = data['email']
        
        if 'password' in data and data['password']:
            user.set_password(data['password'])
        
        db.session.commit()
        
        return jsonify({
            'message': 'Profile updated successfully',
            'user': user.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@user_bp.route('/users', methods=['GET'])
@require_auth
@require_level('admin')
def get_users():
    """Get list of all users (admin only)."""
    try:
        users = User.query.all()
        return jsonify([user.to_dict() for user in users])
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/users/<int:user_id>', methods=['PUT'])
@require_auth
@require_level('admin')
def update_user(user_id):
    """Update user (admin only)."""
    try:
        data = request.get_json()
        user = User.query.get_or_404(user_id)
        
        # Update allowed fields
        if 'user_level' in data:
            user.user_level = data['user_level']
        
        if 'active' in data:
            user.active = data['active']
        
        if 'email' in data:
            # Check if email is already taken by another user
            existing_user = User.query.filter_by(email=data['email']).first()
            if existing_user and existing_user.id != user.id:
                return jsonify({'error': 'Email already exists'}), 400
            user.email = data['email']
        
        db.session.commit()
        
        return jsonify({
            'message': 'User updated successfully',
            'user': user.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
@require_auth
@require_level('admin')
def delete_user(user_id):
    """Delete user (admin only)."""
    try:
        user = User.query.get_or_404(user_id)
        
        # Don't allow deleting the current user
        if user.id == request.current_user.id:
            return jsonify({'error': 'Cannot delete your own account'}), 400
        
        # Delete user sessions first
        UserSession.query.filter_by(user_id=user.id).delete()
        
        db.session.delete(user)
        db.session.commit()
        
        return jsonify({'message': 'User deleted successfully'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@user_bp.route('/check-auth', methods=['GET'])
@require_auth
def check_auth():
    """Check if user is authenticated."""
    return jsonify({
        'authenticated': True,
        'user': request.current_user.to_dict()
    })

@user_bp.route('/init-admin', methods=['POST'])
def init_admin():
    """Initialize admin user if no users exist."""
    try:
        # Check if any users exist
        if User.query.count() > 0:
            return jsonify({'error': 'Admin user already exists'}), 400
        
        # Create default admin user
        admin_user = User(
            username='admin',
            email='admin@lcindex.com',
            user_level='developer'
        )
        admin_user.set_password('admin123')
        
        db.session.add(admin_user)
        db.session.commit()
        
        return jsonify({
            'message': 'Admin user created successfully',
            'username': 'admin',
            'password': 'admin123',
            'user': admin_user.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

