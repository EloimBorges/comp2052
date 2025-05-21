from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user





# Cambios
from app.forms import ItemForm, ChangePasswordForm
from app.models import db, Item, User


# Blueprint principal
main = Blueprint('main', __name__)

@main.route('/')
def index():
    """
    Página de inicio pública.
    """
    return render_template('index.html')


@main.route('/dashboard')
@login_required
def dashboard():
    """
    Muestra los ítems del usuario según su rol.
    """
    if current_user.role.name == 'Admin':
        items = Item.query.all()
    elif current_user.role.name == 'Owner':
        items = Item.query.filter_by(owner_id=current_user.id).all()
    else:  # Usuario regular
        items = []  # Sin permisos para ver ítems

    return render_template('dashboard.html', items=items)


@main.route('/items/nuevo', methods=['GET', 'POST'])
@login_required
def crear_item():
    """
    Crea un nuevo ítem. Solo permitido para Owner o Admin.
    """
    if current_user.role.name not in ['Owner', 'Admin']:
        flash('No tienes permiso para crear ítems.')
        return redirect(url_for('main.dashboard'))

    form = ItemForm()

    if form.validate_on_submit():
        item = Item(
            nombre=form.nombre.data,
            categoria=form.categoria.data,
            cantidad=form.cantidad.data,
            precio_estimado=form.precio_estimado.data,
            ubicacion=form.ubicacion.data,
            fecha_adquisicion=form.fecha_adquisicion.data,
            owner_id=current_user.id
        )
        db.session.add(item)
        db.session.commit()
        flash("Ítem creado con éxito.")
        return redirect(url_for('main.dashboard'))

    return render_template('item_form.html', form=form)


@main.route('/items/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_item(id):
    """
    Edita un ítem existente si el usuario es su dueño o admin.
    """
    item = Item.query.get_or_404(id)

    if current_user.role.name != 'Admin' and item.owner_id != current_user.id:
        flash('No tienes permiso para editar este ítem.')
        return redirect(url_for('main.dashboard'))

    form = ItemForm(obj=item)

    if form.validate_on_submit():
        form.populate_obj(item)
        db.session.commit()
        flash("Ítem actualizado con éxito.")
        return redirect(url_for('main.dashboard'))

    return render_template('item_form.html', form=form, editar=True)


@main.route('/items/<int:id>/eliminar', methods=['POST'])
@login_required
def eliminar_item(id):
    """
    Elimina un ítem si el usuario es su dueño o admin.
    """
    item = Item.query.get_or_404(id)

    if current_user.role.name != 'Admin' and item.owner_id != current_user.id:
        flash('No tienes permiso para eliminar este ítem.')
        return redirect(url_for('main.dashboard'))

    db.session.delete(item)
    db.session.commit()
    flash("Ítem eliminado con éxito.")
    return redirect(url_for('main.dashboard'))


@main.route('/cambiar-password', methods=['GET', 'POST'])
@login_required
def cambiar_password():
    """
    Permite al usuario autenticado cambiar su contraseña.
    """
    form = ChangePasswordForm()

    if form.validate_on_submit():
        if not current_user.check_password(form.old_password.data):
            flash('La contraseña actual es incorrecta.')
            return render_template('cambiar_password.html', form=form)

        current_user.set_password(form.new_password.data)
        db.session.commit()
        flash('✅ Contraseña actualizada con éxito.')
        return redirect(url_for('main.dashboard'))

    return render_template('cambiar_password.html', form=form)


@main.route('/usuarios')
@login_required
def listar_usuarios():
    """
    Lista todos los usuarios. Solo accesible para Admin.
    """
    if current_user.role.name != 'Admin':
        flash("No tienes permiso para ver esta página.")
        return redirect(url_for('main.dashboard'))

    usuarios = User.query.join(User.role).all()
    return render_template('usuarios.html', usuarios=usuarios)