((function() {
    'use strict';

    /*@ngInject*/
    function RepositoryUsers(model, common, authToken, AbstractRepository) {
        var repoName = model.repos.users.entity;
        var $http = common.$http;

        /* Implementation */
        function createRepo() {
            var service = {};
            var base = new AbstractRepository(repoName);

            service.create = function(user) {
                return $http.post('/api/users/create', user)
                    .then(function(res) {
                        authToken.setToken(res.data.token);
                        return res.data;
                    }, function(res){
                        return res.data;
                        //console.log(res);
                    });
            };

            service.login = function(user) {
            	var credentials = {
            		usuario: user.usuario,
            		clave: user.clave
            	};

                return $http.post('/auth/login', credentials).then(function(res) {
                    authToken.setToken(res.data.token);
                    return res.data;
                });
            };

            service.list = base.list;
            service.getById = base.getById;
            service.getSchema = base.getSchema;

            return service;
        }

        return {
            create: createRepo // factory function to create the repository
        };

    }

    angular
        .module('hiraApp.data')
        .factory('repository.users', RepositoryUsers);
})());
