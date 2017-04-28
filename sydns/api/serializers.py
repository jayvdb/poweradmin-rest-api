from rest_framework import serializers
from django.db import transaction
from sydns.api.models import Domain, Record, Zone, User


class DomainSerializer(serializers.ModelSerializer):

    @transaction.atomic
    def create(self, validated_data):
        """
        Link user to the created domain through a record in the in the
        intermediate "zones" table.
        """
        domain = super().create(validated_data)

        owner = User.objects.get(username__iexact=self.request.user.username)
        Zone.objects.create(domain=domain, owner=owner.id)

        return domain

    class Meta:
        lookup_field = 'name'
        model = Domain
        fields = ('name', 'type',)
        read_only_fields = ('type',)


class RecordSerializer(serializers.ModelSerializer):
    domain = serializers.SlugRelatedField(
        queryset=Domain.objects.all(), slug_field='name'
    )

    class Meta:
        model = Record
        fields = ('name', 'type', 'content', 'ttl', 'prio', 'domain')


class ZoneSerializer(serializers.ModelSerializer):

    class Meta:
        model = Zone
        fields = ('domain', 'owner')
