((function() {

    'use strict';

    /*@ngInject*/
    function SignupCtrl(Auth, common, $scope) {
        var vm = this;
        var $window = common.$window;
        var $state = common.$state;

        $scope.user = {};
        $scope.errors = {};

        function register(form) {
            $scope.submitted = true;

            if (form.$valid) {
                var user = {
                    nombre: $scope.user.nombre,
                    correo: $scope.user.correo,
                    clave: $scope.user.clave,
                    usuario: $scope.user.usuario
                };
                
                //console.log(user);
                Auth.createUser(user)
                    .then(function() {
                        $state.go('dashboard');
                    }, function(err) {
                        $scope.errors = {};

                        // Update validity of form fields that match the mongoose errors
                        angular.forEach(err.errors, function(error, field) {
                            form[field].$setValidity('mongoose', false);
                            $scope.errors[field] = error.message;
                        });
                    });
            }
        }

        function loginOauth(provider) {
            $window.location.href = '/auth/' + provider;
        }

        vm.register = register;
        vm.loginOauth = loginOauth;
    }

    angular.module('hiraApp.auth.signup')
        .controller('SignupCtrl', SignupCtrl);

})());
