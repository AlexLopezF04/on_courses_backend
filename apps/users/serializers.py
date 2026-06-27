from rest_framework import serializers

from apps.users.models import AccessLog, ProfessorProfile, StudentProfile, User


class StudentProfileSerializer(serializers.ModelSerializer):
    """Serializer para el perfil de estudiante (anidado en User)."""
    class Meta:
        model = StudentProfile
        exclude = ['user']


class ProfessorProfileSerializer(serializers.ModelSerializer):
    """Serializer para el perfil de profesor (anidado en User)."""
    class Meta:
        model = ProfessorProfile
        exclude = ['user']


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer de lectura para usuarios.
    Incluye el perfil correspondiente según el rol.
    """
    student_profile = StudentProfileSerializer(read_only=True)
    professor_profile = ProfessorProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'role', 'phone', 'is_active', 'date_joined',
            'student_profile', 'professor_profile'
        ]


class UserWriteSerializer(serializers.ModelSerializer):
    """Serializer para crear y actualizar usuarios."""
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'first_name',
            'last_name', 'role', 'phone'
        ]

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        return super().update(instance, validated_data)


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer para registro de nuevos usuarios.
    No requiere rol (se asigna 'student' por defecto).
    """
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'password_confirm',
            'first_name', 'last_name'
        ]

    def validate(self, data):
        if data['password'] != data.pop('password_confirm'):
            raise serializers.ValidationError('Las contraseñas no coinciden')
        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class AccessLogSerializer(serializers.ModelSerializer):
    """Serializer para el registro de sesiones."""
    class Meta:
        model = AccessLog
        fields = '__all__'
