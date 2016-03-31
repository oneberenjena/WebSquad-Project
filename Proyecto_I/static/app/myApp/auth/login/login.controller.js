((function () {

    'use strict';

    /*@ngInject*/
    function LoginCtrl(Auth, common) {
        var vm = this;
        var $window = common.$window;
        var $state = common.$state;

        vm.user = {};
        vm.errors = {};

        vm.logout = Auth.logout;
        vm.isLoggedIn = Auth.isLoggedIn;

        function login(form) {
            vm.submitted = true;

            if (form.$valid) {
                Auth.login({
                    usuario: vm.user.username,
                    clave: vm.user.password
                })
                    .then(function (res) {
                        //datacontext.users.getById()
                    })
                    .catch(function (err) {
                        vm.errors.other = err.message;
                    });
            }
        }

        function loginOauth(provider) {
            $window.location.href = '/auth/' + provider;
        }

        vm.login = login;
        vm.loginOauth = loginOauth;
    }

    angular.module('hiraApp.auth.login')
        .controller('LoginCtrl', LoginCtrl);
})());

