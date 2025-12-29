"""
Docstring for Microsprings-Microservices.shared.utils.enums
"""

"""
Shared enums across all microservices
Copy the enums you need into your services
"""

from django.db import models

class DepartmentChoices(models.TextChoices):
    RM_STORE = 'rm_store', 'Raw Material Store'
    COILING = 'coiling', 'Coiling Department'
    TEMPERING = 'tempering', 'Tempering Department'
    PLATING = 'plating', 'Plating Department'
    PACKING = 'Packing', 'Packing Department'
    FG_STORE = 'fg_store', 'Finished Goods Store'
    QUALITY = 'quality', 'Quality Control'
    MAINTENANCE = 'maintenance', 'Maintenance'
    ADMIN = 'admin', 'Administration'


class ShiftChoices(models.TextChoices):
    SHIFT_I = 'I', 'Shift I (9AM-5PM)'
    SHIFT_II = 'II', 'Shift II (5PM-2AM)'
    SHIFT_III = 'III', 'Shift III (2AM-9AM)'

class RoleHierarchyChoices(models.TextChoices):
    ADMIN = 'admin', 'Administrator'
    MANAGER = 'manager', 'Manager'
    SUPERVISOR = 'supervisor', 'Supervisor'
    OPERATOR = 'operator', 'Operator'
    RM_STORE_MANAGER = 'rm_store_manager', 'RM Store Manager'
    FG_STORE_MANAGER = 'fg_store_manager', 'FG Store Manager'
    QC_INSPECTOR = 'qc_inspector', 'QC Inspector'