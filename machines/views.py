# App de gestion des machines pour re2o
# Gabriel Détraz
# Gplv2
from django.shortcuts import render, redirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.context_processors import csrf
from django.template import Context, RequestContext, loader
from django.contrib import messages

from .models import NewMachineForm, EditMachineForm, EditInterfaceForm, AddInterfaceForm, NewInterfaceForm
from .models import Machine, Interface, IpList
from users.models import User
from users.views import has_access

def unassign_ips(user):
    machines = Interface.objects.filter(machine=Machine.objects.filter(user=user))
    for machine in machines:
        unassign_ipv4(machine)
    return

def assign_ips(user):
    """ Assign une ipv4 aux machines d'un user """
    machines = Interface.objects.filter(machine=Machine.objects.filter(user=user))
    for machine in machines:
        if not machine.ipv4:
            interface = assign_ipv4(machine)
            interface.save()
    return

def free_ip():
    """ Renvoie la liste des ip disponibles """
    return IpList.objects.filter(interface__isnull=True)

def assign_ipv4(interface):
    """ Assigne une ip à l'interface """
    free_ips = free_ip()
    if free_ips:
        interface.ipv4 = free_ips[0]
    return interface

def unassign_ipv4(interface):
    interface.ipv4 = None
    interface.save()

def is_active(interface):
    machine = interface.machine
    user = machine.user
    return machine.active and has_access(user) 

def form(ctx, template, request):
    c = ctx
    c.update(csrf(request))
    return render_to_response(template, c, context_instance=RequestContext(request))

def new_machine(request, userid):
    try:
        user = User.objects.get(pk=userid)
    except User.DoesNotExist:
        messages.error(request, u"Utilisateur inexistant" )
        return redirect("/machines/")
    machine = NewMachineForm(request.POST or None)
    interface = NewInterfaceForm(request.POST or None) 
    if machine.is_valid() and interface.is_valid():
        new_machine = machine.save(commit=False)
        new_machine.user = user
        new_machine.save()
        new_interface = interface.save(commit=False)
        new_interface.machine = new_machine
        if free_ip():
            new_interface = assign_ipv4(new_interface)
        else:
            messages.error(request, u"Il n'y a plus d'ip disponibles")
        new_interface.save()
        messages.success(request, "La machine a été crée")
        return redirect("/users/")
    return form({'machineform': machine, 'interfaceform': interface}, 'machines/machine.html', request)

def edit_machine(request, interfaceid):
    try:
        interface = Interface.objects.get(pk=interfaceid)
    except Interface.DoesNotExist:
        messages.error(request, u"Interface inexistante" )
        return redirect("/machines")
    machine_form = EditMachineForm(request.POST or None, instance=interface.machine)
    interface_form = EditInterfaceForm(request.POST or None, instance=interface)
    if machine_form.is_valid() and interface_form.is_valid():
        machine_form.save()
        interface_form.save()
        messages.success(request, "La machine a été modifiée")
        return redirect("/machines/")
    return form({'machineform': machine_form, 'interfaceform': interface_form}, 'machines/machine.html', request)

def new_interface(request, machineid):
    try:
        machine = Machine.objects.get(pk=machineid)
    except Machine.DoesNotExist:
        messages.error(request, u"Machine inexistante" )
        return redirect("/machines")
    interface_form = AddInterfaceForm(request.POST or None)
    machine_form = EditMachineForm(request.POST or None, instance=machine)
    if interface_form.is_valid() and machine_form.is_valid():
        machine_form.save()
        new_interface = interface_form.save(commit=False)
        new_interface.machine = machine
        new_interface.save()
        messages.success(request, "L'interface a été ajoutée")
        return redirect("/machines/")
    return form({'machineform': machine_form, 'interfaceform': interface_form}, 'machines/machine.html', request)

def index(request):
    machine_list = Interface.objects.order_by('pk')
    return render(request, 'machines/index.html', {'machine_list': machine_list})
