import os
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Database, Table, Column, Row 

# Página de login
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'main/login.html')

# Página de cadastro
def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            return redirect('dashboard')
    return render(request, 'main/register.html')

# Dashboard principal@login_required
def dashboard(request):
    databases = Database.objects.filter(owner=request.user)
    return render(request, 'main/dashboard.html', {'databases': databases})

# Criar um banco de dados@login_required
@login_required
def create_database(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()  # Garantir que está pegando o nome
        if name and not Database.objects.filter(name=name, owner=request.user).exists():
            Database.objects.create(name=name, owner=request.user)
        return redirect('dashboard') 
    return redirect('dashboard')  

# Atualizar nome do banco de dados@login_required
def update_database(request, db_id):
    if request.method == 'POST':
        database = Database.objects.get(id=db_id, owner=request.user)
        database.name = request.POST['name']
        database.save()
    return redirect('dashboard')

# Excluir banco de dados@login_required
def delete_database(request, db_id):
    database = Database.objects.get(id=db_id, owner=request.user)
    database.delete()
    return redirect('dashboard')

# Criar uma tabela@login_required
def create_table(request, db_id):
    if request.method == 'POST':
        database = Database.objects.get(id=db_id, owner=request.user)
        Table.objects.create(name=request.POST['name'], database=database)
    return redirect('dashboard')

# Atualizar nome da tabela@login_required
def update_table(request, table_id):
    if request.method == 'POST':
        table = Table.objects.get(id=table_id)
        table.name = request.POST['name']
        table.save()
    return redirect('dashboard')

# Excluir tabela@login_required
def delete_table(request, table_id):
    table = Table.objects.get(id=table_id)
    table.delete()
    return redirect('dashboard')

# Criar uma coluna@login_required
def create_column(request, table_id):
    if request.method == 'POST':
        table = Table.objects.get(id=table_id)
        Column.objects.create(name=request.POST['name'], table=table, data_type=request.POST['data_type'])
    return redirect('dashboard')

# Atualizar nome da coluna@login_required
def update_column(request, column_id):
    if request.method == 'POST':
        column = Column.objects.get(id=column_id)
        column.name = request.POST['name']
        column.save()
    return redirect('dashboard')

# Excluir coluna@login_required
def delete_column(request, column_id):
    column = Column.objects.get(id=column_id)
    column.delete()
    return redirect('dashboard')

# Inserir dados@login_required
def insert_data(request, table_id):
    if request.method == 'POST':
        table = Table.objects.get(id=table_id)
        data = request.POST.dict()
        data.pop('csrfmiddlewaretoken', None)
        Row.objects.create(table=table, data=data)
    return redirect('dashboard')

# Atualizar dados@login_required
def update_data(request, row_id):
    if request.method == 'POST':
        row = Row.objects.get(id=row_id)
        data = request.POST.dict()
        data.pop('csrfmiddlewaretoken', None)
        row.data = data
        row.save()
    return redirect('dashboard')

# Excluir dados@login_required
def delete_data(request, row_id):
    row = Row.objects.get(id=row_id)
    row.delete()
    return redirect('dashboard')
