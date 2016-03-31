((function () {
    'use strict';

    /*@ngInject*/
    function RepositoryGroups(AbstractRepository, model) {
        var repoName = model.repos.groups.entity;

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
        .factory('repository.groups', RepositoryGroups);
})());