# accounts/views.py
import qrcode
import os
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import QRCode, Formulario

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.GET.get('next', 'dashboard')  # Redirige a dashboard después de loguearse
            return redirect(next_url)
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')  

def generar_qr(request):
    if request.method == 'POST':
        cantidad = int(request.POST.get('cantidad', 1))  # Obtener la cantidad de QR
        qr_folder = os.path.join(settings.MEDIA_ROOT, 'qr_codes')
        os.makedirs(qr_folder, exist_ok=True)  # Crear la carpeta si no existe

        for i in range(cantidad):
            # Crear un folio único
            folio = f"QR-{QRCode.objects.count() + 1}"

            # Generar el QR con el folio
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(f"http://127.0.0.1:8000/validar-qr/{folio}/")  # URL del QR
            qr.make(fit=True)

            # Guardar el QR como archivo PNG
            qr_filename = f"{folio}.png"
            qr_filepath = os.path.join(qr_folder, qr_filename)
            qr_image = qr.make_image(fill_color="black", back_color="white")
            qr_image.save(qr_filepath)

            # Guardar el QR en la base de datos
            QRCode.objects.create(folio=folio)

        return render(request, 'generar_qr.html', {'success': True})

    return render(request, 'generar_qr.html')

def validar_qr(request, folio):
    qr = get_object_or_404(QRCode, folio=folio)

    if qr.usado:
        # Renderizar un mensaje estilizado si el QR ya fue usado
        return render(request, 'mensaje_baja.html', {'folio': folio})

    # Redirigir al formulario si el QR no ha sido usado
    return render(request, 'formulario.html', {'folio': folio})

def formulario_qr(request, folio):
    qr = get_object_or_404(QRCode, folio=folio)

    # Verificar si el QR ya fue utilizado
    if qr.usado:
        # Redirigir al mensaje de "Equipo Dado de Baja"
        return render(request, 'mensaje_baja.html', {'folio': folio})

    if request.method == 'POST':
        # Verificar nuevamente si el QR ya fue utilizado (por seguridad)
        if qr.usado:
            return render(request, 'mensaje_baja.html', {'folio': folio})

        # Obtener los datos del formulario
        pzas = int(request.POST.get('pzas', 0))
        descripcion = request.POST.get('descripcion')
        modelo = request.POST.get('modelo')
        numero_serie = request.POST.get('numero_serie')
        activo_smn = request.POST.get('activo_smn')
        sucursal = request.POST.get('sucursal')

        # Crear el registro en el modelo Formulario
        Formulario.objects.create(
            pzas=pzas,
            descripcion=descripcion,
            modelo=modelo,
            numero_serie=numero_serie,
            activo_smn=activo_smn,
            sucursal=sucursal,
            qr=qr
        )

        # Cambiar el estado del QR a "usado" solo después de guardar los datos
        qr.usado = True
        qr.save()

        # Redirigir al template de mensaje_baja.html
        return render(request, 'mensaje_baja.html', {'folio': folio})

    return render(request, 'formulario.html', {'folio': folio})

def seleccionar_lotes(request):
    return render(request, 'seleccionar_lotes.html')

def historial_bajas(request):
    return render(request, 'historial_bajas.html')
