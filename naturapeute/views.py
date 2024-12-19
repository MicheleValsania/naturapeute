from django.views.generic import TemplateView, ListView, View
from django.views.generic.base import RedirectView, reverse
from django.shortcuts import redirect, reverse,render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.db.models import Q
from .models import Therapist

import vobject

from .models import Therapist, Symptom, Practice


class HomeView(TemplateView):

    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        therapists = Therapist.members.all()
        context["therapistsCount"] = therapists.count()
        context["therapists"] = therapists[:5]
        context["practices"] = Practice.objects.all()
        return context


class TherapistByPractice(ListView):
    template_name = "therapists.html"
    model = Therapist
    context_object_name = "therapists"
    queryset = Therapist.members.all()

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(practice__slug__in=self.kwargs.practice)


class TherapistsView(ListView):
    template_name = "therapists.html"
    model = Therapist
    context_object_name = "therapists"
    queryset = Therapist.members.all()

    def get(self, request, *args, **kwargs):
        practice_name = self.request.GET.get("practice")
        if practice_name:
            try:
                practice = Practice.objects.get(name=practice_name)
            except Practice.DoesNotExist:
                pass
            else:
                return redirect("therapists_practice", practice.slug)
        return super().get(request, *args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        params = self.request.GET
        symptom_name = params.get("symptom")
        practice_slug = self.kwargs.get("practice_slug")
        if practice_slug:
            practice = Practice.objects.get(slug=practice_slug)
            qs = qs.filter(Q(practices__in=[practice]) | Q(practice=practice)).distinct()
        if symptom_name:
            symptoms = Symptom.objects.search(symptom_name)
            qs = qs.filter(symptoms__in=symptoms).distinct()
        return qs


class TherapistView(TemplateView):
    template_name = "therapist.html"

    def get_context_data(self, **kwargs):
        slug = f"{self.kwargs['slug0']}/{self.kwargs['slug1']}"
        try:
            therapist = Therapist.mixed.get(slug=slug)
        except Therapist.DoesNotExist:
            raise Http404(f"Therapist not found with slug {slug}")
        return {"therapist": therapist}

    def get(self, request, *args, **kwargs):
        therapist = self.get_context_data()["therapist"]
        if therapist.membership == "pending":
            return HttpResponseRedirect(reverse("therapists"))
        else:
            return super().get(request, *args, **kwargs)


class TherapistVcardView(View):
    def get(self, *args, **kwargs):
        card = vobject.vCard()
        therapist = Therapist.mixed.get(
            slug=f"{self.kwargs['slug0']}/{self.kwargs['slug1']}"
        )
        office = therapist.offices.first()
        card.add("n")
        card.n.value = vobject.vcard.Name(
            family=therapist.lastname, given=therapist.firstname
        )
        card.add("email")
        card.email.value = therapist.email
        card.add("adr")
        card.adr.value = vobject.vcard.Address(
            street=office.street,
            city=office.city,
            code=office.zipcode,
            country=office.country,
        )
        response = HttpResponse(str(card), content_type="text/vcard")
        response["Content-Disposition"] = f'attachment; filename="{therapist}.vcf"'
        return response
        raise Error("WIP Implementing fields and returning response")


class TherapistOldView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return f"/therapeutes/{kwargs['slug0']}/{kwargs['slug1']}/"
