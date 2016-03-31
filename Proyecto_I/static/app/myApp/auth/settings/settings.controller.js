((function () {

    'use strict';

    function SettingsCtrl(Auth) {
        var vm = this;

        vm.errors = {};

        function changePassword(form) {
            vm.submitted = true;
            if (form.$valid) {
                Auth.changePassword(vm.user.oldPassword, vm.user.newPassword)
                    .then(function () {
                        vm.message = 'Password successfully changed.';
                    })
                    .catch(function () {
                        form.password.$setValidity('mongoose', false);
                        vm.errors.other = 'Incorrect password';
                        vm.message = '';
                    });
            }
        }

        vm.changePassword = changePassword;
    }

    angular.module('hiraApp.auth.settings')
        .controller('SettingsCtrl', SettingsCtrl);

})());

