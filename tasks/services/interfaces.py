from abc import ABC, abstractmethod
from django.contrib.auth.models import User

class ITaskService(ABC):

    @abstractmethod
    def get_user_tasks(self, user: User):
        pass

    @abstractmethod
    def get_pending_tasks(self, user, limit=6):
        pass

    @abstractmethod
    def get_completed_tasks(self, user, limit=6):
        pass

    @abstractmethod
    def mark_task_as_completed(self, task_id, user: User):
        pass

class ICategoryService(ABC):

    @abstractmethod
    def get_all_categories(self):
        pass

    @abstractmethod
    def assign_random_color_to_category(self):
        pass

class IAuthService(ABC):
    @abstractmethod
    def logout_user(self, user: User):
        pass
