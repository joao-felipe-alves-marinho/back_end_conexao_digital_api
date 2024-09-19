from django.contrib import admin

from .models import User, Interesse, FormacaoAcademica, ExperienciaProfissional, Habilidade, Projeto


# Register your models here.
@admin.register(Interesse)
class InteresseAdmin(admin.ModelAdmin):
    pass


class InteresseInLine(admin.TabularInline):
    model = Interesse.users.through
    extra = 0


class FormacaoAcademicaInLine(admin.StackedInline):
    model = FormacaoAcademica
    extra = 0


class ExperienciaProfissionalInLine(admin.StackedInline):
    model = ExperienciaProfissional
    extra = 0


class HabilidadeInLine(admin.StackedInline):
    model = Habilidade
    extra = 0


class ProjetoInLine(admin.StackedInline):
    model = Projeto
    extra = 0



@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Informações Pessoais", {
            "fields": (
                "nome",
                "email",
                "ano_nascimento",
                "genero",
                "telefone",
                "deficiencia",
            )
        }),
        ("Resumo", {"fields": ("resumo",)})
    )
    inlines = [
        InteresseInLine,
        FormacaoAcademicaInLine,
        ExperienciaProfissionalInLine,
        HabilidadeInLine,
        ProjetoInLine
    ]
