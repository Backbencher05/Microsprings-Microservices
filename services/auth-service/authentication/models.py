from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from .utils.enums import DepartmentChoices, ShiftChoices, RoleHierarchyChoices

# Create your models here.

class CustomeUser(AbstractUser):
    """
    Docstring for CustomeUser
    
    Custom User model extending Django's AbstractUser

    why: we want email-based login instead of username
    Changes from default:
    - Email is required and unique
    - Email is used to login (not username)
    """

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Tell Django to use email for login (not username)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        db_table = 'auth_user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.first_name}{self.last_name} ({self.email})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
    
class UserProfile(models.Model):
    """
    Docstring for UserProfile
    
    Extend user profile information for MSP-ERP

    Relationship: One-to-One with CustomUser
    - Each user has exactly ONE profile
    - Each profile belongs to exactly ONE user
    """
    user = models.OneToOneField(
        CustomeUser,
        on_delete=models.CASCADE,
        related_name='profile' 
    )

    # Employee Information
    employee_id = models.CharField(max_length=20, unique=True)
    designation = models.CharField(max_length=100)
    department = models.CharField(
        max_length=20,
        choices=DepartmentChoices.choices 
    )
    shift = models.CharField(
        max_length=10,
        choices=ShiftChoices.choices,
        null=True,
        blank=True 
    )
    date_of_joining = models.DateField()
    phone_number = models.CharField(max_length=15)
    is_active = models.BooleanField(default=True)

    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    def __str__(self):
        return f"{self.user.full_name} - {self.employee_id}"


class Role(models.Model):
    """
    Hierarchical role-based access control for MSP-ERP

    Purpose: Define user roles and their permissions
    Ex: Admin, Manager, Supervisor, Operator
    """
    name = models.CharField(
        max_length=50,
        choices=RoleHierarchyChoices.choices,
        unique=True 
    )
    description = models.TextField()
    hirarchy_level = models.IntegerField(
        default=5,
        help_text="Lower number = higher authority (Admin=1, Operator=5)"
    )
    permissions = models.JSONField(
        default=dict,
        null=True,
        blank=True,
        help_text="Module-specific permissions as JSON"
    )

    # Department restriction (which department this role can access)
    restricted_departments = models.JSONField(
        default=list,
        null= True,
        blank=True,
        help_text="Departments this role can access (empty = all department)"
    )

    class Meta:
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'
        ordering = ['hierarchy_level'] # Lower level first (Admin before Operator)

    def __str__(self):
        return self.get_name_display()
    
    def can_access_department(self, department):
        """
        check if role can access specific department

        Args:
            department: Department code (e.g., 'coiling', 'rm_store')

        Returns: 
            True if role can access, False otherwise
        """
        if not self.restricted_departments:
            return True # No restrictions = access all departments
        return department in self.restricted_departments