socialModule.service('foroService', ['$q', '$http', function($q, $http) {

    this.AComentar = function(fPublicacion) {
        return  $http({
          url: "foro/AComentar",
          data: fPublicacion,
          method: 'POST',
        });
    //    var labels = ["/VPrincipal", "/VComentariosPagina", ];
    //    var res = labels[0];
    //    var deferred = $q.defer();
    //    deferred.resolve(res);
    //    return deferred.promise;
    };

    this.AElimForo = function(args) {
        if(typeof args == 'undefined') args={};
        return $http({
          url: 'foro/AElimForo',
          method: 'POST',
          data: args
        });
    //    var labels = ["/VForos", "/VForo", ];
    //    var res = labels[0];
    //    var deferred = $q.defer();
    //    deferred.resolve(res);
    //    return deferred.promise;
    };
    this.APublicar = function(fPublicacion) {
        return  $http({
          url: "foro/APublicar",
          data: fPublicacion,
          method: 'POST',
        });
    //    var labels = ["/VForo", "/VPublicacion", ];
    //    var res = labels[0];
    //    var deferred = $q.defer();
    //    deferred.resolve(res);
    //    return deferred.promise;
    };

    this.AgregForo = function(fForo) {
        return  $http({
          url: "foro/AgregForo",
          data: fForo,
          method: 'POST',
        });
    //    var labels = ["/VForos", "/VForos", ];
    //    var res = labels[0];
    //    var deferred = $q.defer();
    //    deferred.resolve(res);
    //    return deferred.promise;
    };

    this.VComentariosPagina = function(args) {
        if(typeof args == 'undefined') args={};
        return $http({
          url: 'foro/VComentariosPagina',
          method: 'GET',
          params: args
        });
    //    var res = {};
    //    var deferred = $q.defer();
    //    deferred.resolve(res);
    //    return deferred.promise;
    };

    this.VForo = function(args) {
        if(typeof args == 'undefined') args={};
        return $http({
          url: 'foro/VForo',
          method: 'GET',
          params: args
        });
    //    var res = {};
    //    var deferred = $q.defer();
    //    deferred.resolve(res);
    //    return deferred.promise;
    };

    this.VForos = function(args) {
        if(typeof args == 'undefined') args={};
        return $http({
          url: 'foro/VForos',
          method: 'GET',
          params: args
        });
    //    var res = {};
    //    var deferred = $q.defer();
    //    deferred.resolve(res);
    //    return deferred.promise;
    };

    this.VPublicacion = function(args) {
        if(typeof args == 'undefined') args={};
        return $http({
          url: 'foro/VPublicacion',
          method: 'GET',
          params: args
        });
    //    var res = {};
    //    var deferred = $q.defer();
    //    deferred.resolve(res);
    //    return deferred.promise;
    };
    
    this.AObtenerComentarios = function(args) {
        if(typeof args == 'undefined') args={};
        return $http({
          url: 'foro/AObtenerComentarios',
          method: 'GET',
          params: args
        });
    //    var res = {};
    //    var deferred = $q.defer();
    //    deferred.resolve(res);
    //    return deferred.promise;
    };
}]);