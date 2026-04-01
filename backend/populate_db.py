from werkzeug.security import generate_password_hash
from models import db, User, Budget, Expense


def seed_db():
  # only seed if no users exist (fresh database)
  if User.query.count() > 0:
    return

  # demo user
  user = User(name='Vidhatri', email='vidhatri@example.com',
              password=generate_password_hash('password123'))
  db.session.add(user)
  db.session.flush()  # get user.id before commit

  # budget
  budget = Budget(amount=50000, user_id=user.id)
  db.session.add(budget)

  # sample expenses
  expenses = [
      Expense(amount=1200, category='Food', description='Grocery run', user_id=user.id),
      Expense(amount=500,  category='Transport', description='Uber to office', user_id=user.id),
      Expense(amount=3000, category='Shopping', description='New headphones', user_id=user.id),
      Expense(amount=800,  category='Food', description='Dinner with friends', user_id=user.id),
      Expense(amount=1500, category='Utilities', description='Electricity bill', user_id=user.id),
  ]
  db.session.add_all(expenses)

  db.session.commit()
  print('Database seeded — login: vidhatri@example.com / password123')
