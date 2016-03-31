((function () {
    'use strict';

    /*@ngInject*/
    function datacontext($injector) {

        var service = {};
        //Repository names
        var repoNames = ['users','chats','contacts','groups','memberships','pages'];

        // Get named Repository Ctor (by injection), new it, and initialize it
        function getRepo(repoName) {
            var fullRepoName = 'repository.' + repoName.toLowerCase();
            var factory = $injector.get(fullRepoName);
            return factory.create();
        }

        // Add ES5 property to datacontext for each named repo
        function defineLazyLoadedRepos() {
            repoNames.forEach(function (collection) {
                Object.defineProperty(service, collection, {
                    configurable: true, // will redefine this property once
                    get: function () {
                        // The 1st time the repo is request via this property,
                        // we ask the repositories for it (which will inject it).
                        var repo = getRepo(collection);
                        // Rewrite this property to always return this repo;
                        // no longer redefinable
                        Object.defineProperty(service, collection, {
                            value: repo,
                            configurable: false,
                            enumerable: true
                        });
                        return repo;
                    }
                });
            });
        }

        //Init function setting things up
        function init() {
            defineLazyLoadedRepos();
        }

        init();

        return service;
    }

    angular
        .module('hiraApp.data')
        .factory('datacontext', datacontext);

})());