((function() {
    'use strict';

    /*@ngInject*/
    function AbstractRepository(common, model, metaData, serverSpeaker, ResourcesSvc, Resources) {
        /* jshint validthis:true */
        var $q = common.$q;
        var $http = common.$http;

        /* Implementation */

        function getManager(entity,manager){
            var mng = entity;

            if (mng === 'blocks' || mng === 'views'){
                mng += '.' + manager;
            }

            return mng;
        }

        function list(options) {
            var mng = getManager(this.entityName,options.manager);

            function querySucceeded(res) {
                ResourcesSvc.set(mng,res.data);
                return res.data;
            }

            var filter = options.filter || {};

            var isEmpty = ResourcesSvc.isEmpty(mng);

            if (!isEmpty && !options.forceRemote) {
                return $q.when(Resources[mng]);
            }

            return serverSpeaker
                .use(this.entityName)
                .filter(filter.find)
                .searchTerm(filter.term)
                .manager(mng)
                .execute('list')
                .then(querySucceeded);
        }

        function getSchema() {
            var mng = this.entityName;

            function querySucceeded(res) {
                metaData.init(res.data);
                return res.data[mng];
            }

            var hasItems = metaData.hasItems(mng);

            if (hasItems) {
                return $q.when(metaData.getEntity(mng));
            }

            return serverSpeaker
                .use('metadata')
                .filter()
                .manager(mng)
                .execute()
                .then(querySucceeded);
        }

        function getById(id) {
            return $http.get('api/' + this.entityName + '/show/' + id).then(function(res) {
                return res.data;
            }, queryFailed);
        }

        function create(manager, data) {
            var mng = getManager(this.entityName,manager);
            
            return $http.post('api/' + this.entityName + '/create', data).then(function(res) {
                if (!ResourcesSvc.isEmpty(mng)){
                    ResourcesSvc.add(mng,res.data);
                }

                return res.data;
            }, queryFailed);
        }

        function update(manager, data) {
            var mng = getManager(this.entityName,manager);

            return $http.put('api/' + this.entityName + '/update/' + data._id, data).then(function(res) {
                if (!ResourcesSvc.isEmpty(mng)){
                    ResourcesSvc.update(mng,res.data);
                }

                return res.data;
            }, queryFailed);
        }

        function remove(manager, id) {
            var mng = getManager(this.entityName,manager);

            return $http.delete('api/' + this.entityName + '/remove/' + id).then(function(res) {
                if (!ResourcesSvc.isEmpty(mng)){
                    ResourcesSvc.remove(mng,id);
                }

                return res.data;
            }, queryFailed);
        }

        function queryFailed(error) {
            var msg = 'Error retrieving data. ' + (error.message || '');
            return $q.reject(new Error(msg));
        }

        function Ctor(entityName) {
            // instance members that are stateful
            this.entityName = entityName;
            this.getById = getById.bind(this);
            this.create = create.bind(this);
            this.update = update.bind(this);
            this.remove = remove.bind(this);
            this.getSchema = getSchema.bind(this);
            this.list = list.bind(this);
            this.queryFailed = queryFailed.bind(this); // Bind to self so we establish 'this' as the context
        }

        /* stateless methods that can be shared across all repos */
        Ctor.prototype = {
            constructor: Ctor,
            $q: $q
        };

        return Ctor;
    }

    angular
        .module('hiraApp.data')
        .factory('AbstractRepository', AbstractRepository);

})());
