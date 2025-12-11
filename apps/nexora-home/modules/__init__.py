"""
Nexora Suite - Integrated Modules Package

All business modules are integrated as sub-modules of the main nexora-home application.
Each module maintains its own models, routes, and logic while sharing the main database.

Modules:
- billing: Invoice, payment, and billing management
- crm: Customer relationship management
- inventory: Stock and inventory management
- invoice: Invoice generation and tracking
- expense: Expense tracking and reporting
- bookings: Appointment and booking management
- ... and more

Each module is registered with a unique namespace (/module/<name>/).
"""

__all__ = []
