from datetime import datetime

# Use the application's SQLAlchemy instance to avoid duplicate metadata
from app import db


class Ledger(db.Model):
    __tablename__ = 'ledgers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    accounts = db.relationship('Account', backref='ledger', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat()
        }


class Account(db.Model):
    __tablename__ = 'accounts'
    id = db.Column(db.Integer, primary_key=True)
    ledger_id = db.Column(db.Integer, db.ForeignKey('ledgers.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    account_type = db.Column(db.String(50))
    balance = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    transactions = db.relationship('Transaction', backref='account', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'ledger_id': self.ledger_id,
            'name': self.name,
            'account_type': self.account_type,
            'balance': self.balance,
            'created_at': self.created_at.isoformat()
        }


class JournalEntry(db.Model):
    __tablename__ = 'journal_entries'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.Text)

    transactions = db.relationship('Transaction', backref='journal_entry', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'date': self.date.isoformat(),
            'description': self.description,
            'transactions': [t.to_dict() for t in self.transactions]
        }


class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    journal_entry_id = db.Column(db.Integer, db.ForeignKey('journal_entries.id'), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    is_debit = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'journal_entry_id': self.journal_entry_id,
            'account_id': self.account_id,
            'amount': self.amount,
            'is_debit': self.is_debit,
            'created_at': self.created_at.isoformat()
        }


class BalanceSheet:
    """Simple balance computation helper (not a DB model)."""
    def __init__(self, ledger_id):
        self.ledger_id = ledger_id

    def compute(self):
        # placeholder: real implementation would query accounts and sum balances
        return {
            'ledger_id': self.ledger_id,
            'assets': 0.0,
            'liabilities': 0.0,
            'equity': 0.0
        }
