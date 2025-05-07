from flask import Blueprint, redirect, render_template, request, url_for, flash
from flask_login import current_user, login_required
from app.models import db, Employee, Menu, MenuItem, MenuItemType, Order, Table
from app.forms import AssignTableForm, CloseTableForm, AddItemsForm
from sqlalchemy import not_


bp = Blueprint("orders", __name__, url_prefix="")


@bp.route("/", methods=["POST", "GET"])
@login_required     #to make sure you can only access this if logged in
def index():
    assign_table_form = AssignTableForm()
    close_table_form = CloseTableForm()
    add_items_form = AddItemsForm()

    # tables = Table.query.order_by(Table.number).all()
    employees = Employee.query.order_by(Employee.employee_number).all()
    # orders = Order.query.filter(Order.finished == False).all()          # all active orders

    open_tables = (
    db.session.query(Table)
    .filter(
        not_(Table.id.in_(
            db.session.query(Order.table_id)
            .filter(Order.finished == False)
        ))
    )
    .order_by(Table.number)
    .all()
)


    # filled_table_ids = [order.table_id for order in orders]    # any active order is tied to a table, those tables are currently filled
    # open_tables = [table for table in tables if table.id not in filled_table_ids]   #use filled table to find open tables

    assign_table_form.tables.choices = [(t.id, f"Table number {t.number}") for t in open_tables]
    assign_table_form.servers.choices = [(e.id, f"{e.name}") for e in employees]

    your_orders = Order.query.filter(
        Order.employee_id == current_user.id,
        Order.finished == False
    ).all()

    # menu_items = (
    #     MenuItem.query.join(MenuItemType)
    #     .group_by(MenuItemType.name, MenuItem.id)
    #     .order_by(MenuItemType.name, MenuItem.name)
    # ).all()

    items = (
        db.session.query(MenuItem)
        .join(MenuItemType)
        .order_by(MenuItemType.name, MenuItem.name)
        .all()
    )

    # Required for form validation
    add_items_form.menu_items.choices = [(item.id, f"{item.type.name} - {item.name}") for item in items]

    # For rendering the grouped dropdown manually
    grouped_items = items

    # Populate orders too (assuming active orders)
    add_items_form.order.choices = [(o.id, f"Order #{o.id}") for o in Order.query.filter_by(finished=False).all()]


    if add_items_form.validate_on_submit():
        # Handle form submission here
        selected_items = add_items_form.menu_items.data  # List of IDs
        order_id = add_items_form.order.data
        # Add logic here to associate items with the order...
        return redirect(url_for(".index"))

    if assign_table_form.validate_on_submit():
        table_id = assign_table_form.table.data
        employee_id = assign_table_form.employee.data
        create_order = Order(
            table_id=table_id,
            employee_id=employee_id,
            finished=False
        )
        db.session.add(create_order)
        db.session.commit()
        redirect(url_for(".index"))

    return render_template(
        "orders.html",
        assign_table=assign_table_form,
        your_orders=your_orders,
        close_table=close_table_form,
        add_items=add_items_form,
        items = grouped_items
    )
