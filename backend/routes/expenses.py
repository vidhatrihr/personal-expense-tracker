from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from models import db, Budget, Expense

expenses_bp = Blueprint('expenses', __name__)


@expenses_bp.route('/budget', methods=['GET'])
@login_required
def get_budget():
    budget = current_user.budget
    amount = budget.amount if budget else 0
    return jsonify({'data': {'amount': amount}})


@expenses_bp.route('/budget', methods=['POST'])
@login_required
def set_budget():
    data = request.get_json()
    budget = current_user.budget

    # create budget if not exists, else update
    if not budget:
        budget = Budget(user_id=current_user.id, amount=data['amount'])
        db.session.add(budget)
    else:
        budget.amount = data['amount']

    db.session.commit()
    return jsonify({'message': 'Budget updated', 'data': {'amount': budget.amount}})


@expenses_bp.route('/expenses', methods=['GET'])
@login_required
def get_expenses():
    expenses = current_user.expenses
    result = [
        {'id': e.id, 'amount': e.amount, 'category': e.category, 'description': e.description}
        for e in expenses
    ]
    return jsonify({'data': result})


@expenses_bp.route('/expenses', methods=['POST'])
@login_required
def add_expense():
    data = request.get_json()
    expense = Expense(
        amount=data['amount'],
        category=data['category'],
        description=data['description'],
        user_id=current_user.id
    )
    db.session.add(expense)
    db.session.commit()
    return jsonify({'message': 'Expense added', 'data': {
        'id': expense.id, 'amount': expense.amount,
        'category': expense.category, 'description': expense.description
    }})


@expenses_bp.route('/expenses/<int:expense_id>', methods=['DELETE'])
@login_required
def delete_expense(expense_id):
    expense = Expense.query.get(expense_id)
    db.session.delete(expense)
    db.session.commit()
    return jsonify({'message': 'Expense deleted'})
