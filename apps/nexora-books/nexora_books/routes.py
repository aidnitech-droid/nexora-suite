from flask import render_template, request, redirect, url_for, flash
from . import nexora_books_bp
from .models import db, Ledger, Account, JournalEntry, Transaction


@nexora_books_bp.route('/books/dashboard')
def dashboard():
    ledgers = Ledger.query.all()
    accounts = Account.query.limit(10).all()
    return render_template('nexora_books/dashboard.html', ledgers=ledgers, accounts=accounts)


@nexora_books_bp.route('/books/add-entry', methods=['GET', 'POST'])
def add_entry():
    if request.method == 'POST':
        description = request.form.get('description')
        entries = request.form.getlist('entries')  # simplistic
        je = JournalEntry(description=description)
        db.session.add(je)
        db.session.commit()
        flash('Journal entry created', 'success')
        return redirect(url_for('nexora_books.dashboard'))
    accounts = Account.query.all()
    return render_template('nexora_books/add_entry.html', accounts=accounts)


@nexora_books_bp.route('/books/ledgers')
def view_ledgers():
    ledgers = Ledger.query.all()
    return render_template('nexora_books/ledgers.html', ledgers=ledgers)
