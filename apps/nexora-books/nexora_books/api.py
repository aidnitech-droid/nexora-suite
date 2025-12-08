from flask import jsonify, request
from . import nexora_books_bp
from .models import db, Ledger, Account, JournalEntry, Transaction


@nexora_books_bp.route('/api/books/ledgers', methods=['GET'])
def api_get_ledgers():
    ledgers = Ledger.query.all()
    return jsonify([l.to_dict() for l in ledgers]), 200


@nexora_books_bp.route('/api/books/ledgers', methods=['POST'])
def api_create_ledger():
    data = request.get_json() or {}
    name = data.get('name')
    description = data.get('description')
    if not name:
        return jsonify({'error': 'name required'}), 400
    ledger = Ledger(name=name, description=description)
    db.session.add(ledger)
    db.session.commit()
    return jsonify(ledger.to_dict()), 201


@nexora_books_bp.route('/api/books/accounts', methods=['POST'])
def api_create_account():
    data = request.get_json() or {}
    ledger_id = data.get('ledger_id')
    name = data.get('name')
    if not ledger_id or not name:
        return jsonify({'error': 'ledger_id and name required'}), 400
    account = Account(ledger_id=ledger_id, name=name, account_type=data.get('account_type'))
    db.session.add(account)
    db.session.commit()
    return jsonify(account.to_dict()), 201


@nexora_books_bp.route('/api/books/journal', methods=['POST'])
def api_create_journal_entry():
    data = request.get_json() or {}
    description = data.get('description')
    transactions = data.get('transactions', [])
    je = JournalEntry(description=description)
    db.session.add(je)
    db.session.flush()
    for tx in transactions:
        t = Transaction(journal_entry_id=je.id, account_id=tx['account_id'], amount=tx['amount'], is_debit=tx.get('is_debit', True))
        db.session.add(t)
    db.session.commit()
    return jsonify(je.to_dict()), 201
