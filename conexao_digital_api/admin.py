from django import forms
from django.contrib import admin
from semantic_admin import SemanticModelAdmin, SemanticStackedInline, SemanticTabularInline
from semantic_forms.filters import SemanticFilterSet
import django_filters

from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render
from django.urls import path
from django.http import HttpResponseRedirect

from semantic_forms.forms import SemanticForm
from semantic_forms.fields import SemanticCharField, SemanticTextareaField

from .models import User, Interesse, FormacaoAcademica, ExperienciaProfissional, Habilidade, Projeto


@admin.register(Interesse)
class InteresseAdmin(SemanticModelAdmin):
    pass


class InteresseInLine(SemanticTabularInline):
    model = Interesse.users.through
    extra = 0


class FormacaoAcademicaInLine(SemanticStackedInline):
    model = FormacaoAcademica
    extra = 0


class ExperienciaProfissionalInLine(SemanticStackedInline):
    model = ExperienciaProfissional
    extra = 0


class HabilidadeInLine(SemanticStackedInline):
    model = Habilidade
    extra = 0


class ProjetoInLine(SemanticStackedInline):
    model = Projeto
    extra = 0


class UserFilter(SemanticFilterSet):
    idade_min = django_filters.NumberFilter(field_name="idade", lookup_expr='gte', label="Idade Mínima")
    idade_max = django_filters.NumberFilter(field_name="idade", lookup_expr='lte', label="Idade Máxima")
    interesses = django_filters.ModelMultipleChoiceFilter(
        queryset=Interesse.objects.all(),
        field_name="interesses",
        label="Interesses",
        conjoined=True  # All selected interests must be matched
    )
    curso = django_filters.CharFilter(
        field_name="formacoes_academicas__curso",
        lookup_expr='icontains',
        label="Curso"
    )
    semestre_min = django_filters.NumberFilter(
        field_name="formacoes_academicas__semestre",
        lookup_expr='gte',
        label="Semestre Mínimo"
    )
    semestre_max = django_filters.NumberFilter(
        field_name="formacoes_academicas__semestre",
        lookup_expr='lte',
        label="Semestre Máximo"
    )
    instituicao = django_filters.CharFilter(
        field_name="formacoes_academicas__instituicao",
        lookup_expr='icontains',
        label="Instituição"
    )

    class Meta:
        model = User
        fields = (
            "nome",
            "email",
            "genero",
            "deficiencia",
            "idade_min",
            "idade_max",
            "interesses",
            "curso",
            "semestre_min",
            "semestre_max",
            "instituicao"
        )


@admin.register(User)
class UserAdmin(SemanticModelAdmin):
    filterset_class = UserFilter
    fieldsets = (
        ("Informações Pessoais", {
            "fields": (
                "nome",
                "email",
                "idade",
                "genero",
                "telefone",
                "deficiencia",
            )
        }),
        ("Resumo", {"fields": ("resumo",)})
    )
    inlines = [
        InteresseInLine,
        HabilidadeInLine,
        FormacaoAcademicaInLine,
        ExperienciaProfissionalInLine,
        ProjetoInLine
    ]
    actions = ['send_email']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(is_superuser=False, is_staff=False)

    def send_email(self, request, queryset):
        if 'apply' in request.POST:
            form = EmailForm(request.POST)
            if form.is_valid():
                subject = form.cleaned_data['subject']
                message = form.cleaned_data['message']
                recipients = queryset.values_list('email', flat=True)

                # Send the email
                send_mail(
                    subject,
                    message,
                    'your_email@example.com',  # Sender's email address
                    recipients,
                )

                self.message_user(request, f"Emails enviados para {queryset.count()} usuários.")
                return HttpResponseRedirect(request.get_full_path())
        else:
            form = EmailForm()

        return render(request, 'admin/send_email.html', {'form': form, 'users': queryset})

    send_email.short_description = "Enviar Email para Usuários Selecionados"

    # Override the get_urls method to add a custom view for the email form
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('send-email/', self.admin_site.admin_view(self.send_email), name='send-email'),
        ]
        return custom_urls + urls


class EmailForm(SemanticForm):
    subject = SemanticCharField(label="Assunto do Email")
    message = SemanticTextareaField(label="Mensagem do Email")
