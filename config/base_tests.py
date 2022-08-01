# Python
import os

# Django
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.test import TestCase


class AppBaseTestCase(TestCase):
    """Base Test Case
    This base class for tests allows testing the code corresponding to the functionalities
    that consists only of generic CRUDs
    """

    model = None

    @staticmethod
    def get_default_user():
        """Create Default User"""
        return User.objects.create_user(
            first_name=os.environ.get("TS_FIRST", "Nelson Guillermo"),
            last_name=os.environ.get("TS_LAST", "Agurto"),
            email=os.environ.get("TS_EMAIL", "nelsonguillerm7@solnustec.com"),
            username=os.environ.get("TS_USER", "nelsonguillerm7"),
            password=os.environ.get("TS_PASSWORD", "m*I8TFDfFvrt"),
        )

    def _get_slug_or_pk(self, instance=None):
        if instance:
            return instance.slug if hasattr(instance, "slug") else instance.pk

    def add_permissions_to_user(self, permissions):
        """Add received permissions to user"""
        for permission in permissions:
            permission.user_set.add(self.user)

    def login_default_user(self):
        """Login default user"""
        self.client.login(
            username=os.environ.get("TS_USER", "nelsonguillerm7"),
            password=os.environ.get("TS_PASSWORD", "m*I8TFDfFvrt"),
        )

    def resolve_get_url(self, path, args=None, kwargs=None, follow=False):
        """Resolve get url
        @path: url name to resolve -> string
        @args: list of args -> []
        @kwargs: dictionary of args based in key and values: used in get parameters -> {key: value}
        @follow: True or False value, define whether the request will resolve all redirects that are submitted->Boolean
        """
        if kwargs is None:
            kwargs = {}
        path = reverse(path, args=args) if args else reverse(path)
        url_kwargs = f"{path}?"
        if kwargs:
            for key, value in kwargs.items():
                url_kwargs = f"{url_kwargs}{key}={value}&"
        return self.client.get(url_kwargs, follow=follow)

    def resolve_post_url(self, path, data, args=None, kwargs=None, follow=False):
        """Resolve post url
        @path: url name to resolve -> string
        @args: list of args -> []
        @kwargs: dictionary of args based in key and values: used in get parameters -> {key: value}
        @follow: True or False value, define whether the request will resolve all redirects that are submitted->Boolean
        """
        if kwargs is None:
            kwargs = {}
        path = reverse(path, args=args) if args else reverse(path)
        url_kwargs = f"{path}?"
        if kwargs:
            for key, value in kwargs.items():
                url_kwargs = f"{url_kwargs}{key}={value}&"
        return self.client.post(url_kwargs, data, follow=follow)

    def authorized_user_can_create_object(
        self,
        path,
        data,
        permissions=None,
        args=None,
        get_params=None,
        assertQuery=None,
        assertQuerys=[],
        stop=False,
    ):
        """Test that authorized user can create a object
        @path: url name to resolve -> string
        @data: data dictionary to send the post request ->{key: value}
        @permissions: Permission object to add permissions to default user -> Permission instance
        @args: list of args. For example pk or slug -> []
        @get_params: dictionary of args based in key and values: used in get parameters -> {key: value}
        @assertQuery: QuerySet to verify if instance exist-> The expression must evaluate true or false
        @assertQuerys: Groups of QuerySet to assert verify, optional-> The expression contains complete assert
        """

        if permissions:
            self.add_permissions_to_user(permissions)
        self.login_default_user()
        response = self.resolve_get_url(path=path, follow=True, kwargs=get_params)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name="base/base_form.html")
        response = self.resolve_post_url(
            path=path, data=data, follow=True, kwargs=get_params
        )
        if stop:
            breakpoint()
        if assertQuery:
            self.assertTrue(eval(assertQuery))

        for query in assertQuerys:
            eval(query)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name="base/base_detail.html")

    def unauthorized_user_cant_create_objects(
        self, path, data, args=None, get_params=None, assertQuery=None
    ):
        """Test that unauthorized user can't create a object

        @path: url name to resolve -> string
        @data: data dictionary to send the post request ->{key: value}
        @args: list of args. For example pk or slug -> []
        @get_params: dictionary of args based in key and values: used in get parameters -> {key: value}
        @assertQuery: QuerySet to verify if instance exist-> The expression must evaluate true or false
        """

        self.login_default_user()
        response = self.resolve_get_url(path=path)
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, template_name="403.html")
        response = self.resolve_post_url(path=path, data=data, follow=True)
        self.assertTemplateUsed(response, template_name="403.html")

    # List and Detail Test Case

    def authorized_user_can_list_or_detail_objects(
        self, path, args=None, get_parameters=None, assertQuery=None, permissions=None
    ):
        """Test that authorized users can see the list or detail Objects
        @path: url name to resolve -> string
        @args: list of args. For example pk or slug -> []
        @get_params: dictionary of args based in key and values: used in get parameters -> {key: value}
        @assertQuery: QuerySet to verify if instance exist-> The expression must evaluate true or false
        @permissions: Permission object to add permissions to default user -> Permission instance
        """

        if permissions:
            self.add_permissions_to_user(permissions)
        self.login_default_user()
        response = self.resolve_get_url(path=path, args=args)
        self.assertEqual(response.status_code, 200)

    def unauthorized_user_cant_list_or_detail_objects(
        self, path, args=None, get_parameters=None, assertQuery=None, permissions=None
    ):
        """Test that unauthorized users can't see the list or detail of objects
        @path: url name to resolve -> string
        @args: list of args. For example pk or slug -> []
        @get_params: dictionary of args based in key and values: used in get parameters -> {key: value}
        @assertQuery: QuerySet to verify if instance exist-> The expression must evaluate true or false
        @permissions: Permission object to add permissions to default user -> Permission instance
        """
        self.login_default_user()
        response = self.resolve_get_url(path=path, args=args)
        self.assertEqual(response.status_code, 403)

    # Update Tests Case

    def authorized_user_can_update_objects(
        self,
        path,
        data,
        permissions=None,
        args=None,
        get_params=None,
        assertQuery=None,
        assertSearch=None,
    ):
        """Test that authorized user can update a object
        @path: url name to resolve -> string
        @data: data dictionary to send the post request ->{key: value}
        @permissions: Permission object to add permissions to default user -> Permission instance
        @args: list of args. For example pk or slug -> []
        @get_params: dictionary of args based in key and values: used in get parameters -> {key: value}
        @assertQuery: QuerySet to verify if instance exist-> The expression must evaluate true or false
        @assertSearch: String to be searched in the response obtained -> String
        """
        if permissions:
            self.add_permissions_to_user(permissions)
        self.login_default_user()
        response = self.resolve_get_url(path=path, args=args)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name="base/base_form.html")
        response = self.resolve_post_url(path=path, args=args, data=data, follow=True)
        if assertSearch:
            self.assertContains(response, assertSearch)
        self.assertEqual(response.status_code, 200)

    def unauthorized_user_cant_update_objects(
        self, path, args=None, get_parameters=None, data={}
    ):
        """Test that authorized user can't update a object
        @path: url name to resolve -> string
        @args: list of args. For example pk or slug -> []
        @get_params: dictionary of args based in key and values: used in get parameters -> {key: value}
        @data: data dictionary to send the post request ->{key: value}
        """
        self.login_default_user()
        response = self.resolve_get_url(path=path, args=args)
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, template_name="403.html")
        response = self.resolve_post_url(path=path, args=args, data=data, follow=True)
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, template_name="403.html")

    # All Tests Case
    def unauthenticated_user_is_redirected_to_login_page(self, path, args=None):
        """Test that an unauthenticated user is redirected to the login page when trying create object
        @path: url name to resolve -> string
        @args: list of args. For example pk or slug -> []
        """

        response = self.resolve_get_url(path=path, args=args, follow=True)
        self.assertTemplateUsed(response, "auth/login.html")
