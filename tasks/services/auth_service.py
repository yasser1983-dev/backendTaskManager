from django.contrib.auth.models import User

class AuthService:
    def logout_user(self, user: User) -> bool:
        """
        Elimina el token de autenticación de un usuario.
        Retorna True si la operación fue exitosa, False en caso contrario.
        """
        if user and hasattr(user, 'auth_token'):
            user.auth_token.delete()
            return True
        return False