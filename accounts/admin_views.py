from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render


@staff_member_required
def admin_tools(request):
    return render(request, "accounts/admin_tools.html")
