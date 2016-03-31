((function () {
    'use strict';

    /*@ngInject*/
    function RepositoryMemberships(AbstractRepository, model) {
        var repoName = model.repos.memberships.entity;

        /* Implementation */
        function createRepo() {
            var service = {};
            var base = new AbstractRepository(repoName);

            service.getById = base.getById;
            service.create = base.create;
            service.update = base.update;
            service.remove = base.remove;
            service.getSchema = base.getSchema;
            service.list = base.list;

            return service;
        }

        return {
            create: createRepo // factory function to create the repository
        };

    }

    angular
        .module('hiraApp.data')
        .factory('repository.memberships', RepositoryMemberships);
})());