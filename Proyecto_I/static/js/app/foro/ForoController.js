socialModule.config(['$routeProvider', function ($routeProvider) {
    $routeProvider.when('/VComentariosPagina/:idPaginaSitio', {
                controller: 'VComentariosPaginaController',
                templateUrl: 'app/foro/VComentariosPagina.html'
            }).when('/VForo/:idForo', {
                controller: 'VForoController',
                templateUrl: 'app/foro/VForo.html'
            }).when('/VForos/:idUsuario', {
                controller: 'VForosController',
                templateUrl: 'app/foro/VForos.html'
            }).when('/VPublicacion/:tipo/:id/:idPadre?', {
                controller: 'VPublicacionController',
                templateUrl: 'app/foro/VPublicacion.html'
            }).when('/p/:nombrePagina', {
                controller: 'PaginaSitioController',
                templateUrl: 'app/paginasSitio/TPaginaSitio.html'
            });
}]);

socialModule.controller('VComentariosPaginaController', 
   ['$scope', '$location', '$route', '$timeout', 'flash', '$routeParams', 'ngDialog', 'foroService', 'identService',
    function ($scope, $location, $route, $timeout, flash, $routeParams, ngDialog, foroService, identService) {
      $scope.msg = '';
      $scope.fPublicacion = {};

      foroService.VComentariosPagina({"idPaginaSitio":$routeParams.idPaginaSitio}).then(function (object) {
        $scope.res = object.data;
        for (var key in object.data) {
            $scope[key] = object.data[key];
        }
        if ($scope.logout) {
            $location.path('/');
        }

        if ($scope.fPublicacion.fecha) {
          $scope.fPublicacion.fecha=new Date($scope.fPublicacion.fecha);
        }

      });
      $scope.VPrincipal1 = function() {
        $location.path('/VPrincipal');
      };

      $scope.fPublicacionSubmitted = false;
      $scope.AComentar0 = function(isValid) {
        $scope.fPublicacionSubmitted = true;
        if (isValid) {
          
          foroService.AComentar($scope.fPublicacion).then(function (object) {
              var msg = object.data["msg"];
              if (msg) flash(msg);
              var label = object.data["label"];
              $location.path(label);
              $route.reload();
          });
        }
      };

$scope.__ayuda = function() {
ngDialog.open({ template: 'ayuda_VComentariosPagina.html',
        showClose: true, closeByDocument: true, closeByEscape: true});
}
    }]);
socialModule.controller('VForoController', 
   ['$scope', '$location', '$route', '$timeout', 'flash', '$routeParams', 'ngDialog', 'ngTableParams', 'foroService', 'identService',
    function ($scope, $location, $route, $timeout, flash, $routeParams, ngDialog, ngTableParams, foroService, identService) {
      $scope.msg = '';
      foroService.VForo({"idForo":$routeParams.idForo}).then(function (object) {
        $scope.res = object.data;
        for (var key in object.data) {
            $scope[key] = object.data[key];
        }
        if ($scope.logout) {
            $location.path('/');
        }
        


      });
      $scope.VPublicacion1 = function(tipo) {
        $location.path('/VPublicacion/'+tipo+"/"+$routeParams.idForo);
      };
      $scope.VForos2 = function(idUsuario) {
        $location.path('/VForos/'+idUsuario);
      };
      $scope.AElimForo3 = function(idForo) {
          
        foroService.AElimForo({"idForo":((typeof idForo === 'object')?JSON.stringify(idForo):idForo)}).then(function (object) {
          var msg = object.data["msg"];
          if (msg) flash(msg);
          var label = object.data["label"];
          $location.path(label);
          $route.reload();
        });};

      $scope.VPublicacion0 = function(tipo,idPublicacion) {
        $location.path('/VPublicacion/'+tipo+"/"+$routeParams.idForo+"/"+idPublicacion);
      };

$scope.__ayuda = function() {
ngDialog.open({ template: 'ayuda_VForo.html',
        showClose: true, closeByDocument: true, closeByEscape: true});
}
    }]);
socialModule.controller('VForosController', 
   ['$scope', '$location', '$route', '$timeout', 'flash', '$routeParams', 'ngDialog', 'ngTableParams', 'foroService', 'identService',
    function ($scope, $location, $route, $timeout, flash, $routeParams, ngDialog, ngTableParams, foroService, identService) {
      $scope.msg = '';
      $scope.fForo = {};

      foroService.VForos({"idUsuario":$routeParams.idUsuario}).then(function (object) {
        $scope.res = object.data;
        for (var key in object.data) {
            $scope[key] = object.data[key];
        }
        if ($scope.logout) {
            $location.path('/');
        }


              var VForo0Data = $scope.res.data0;
              if(typeof VForo0Data === 'undefined') VForo0Data=[];
              $scope.tableParams0 = new ngTableParams({
                  page: 1,            // show first page
                  count: 10           // count per page
              }, {
                  total: VForo0Data.length, // length of data
                  getData: function($defer, params) {
                      $defer.resolve(VForo0Data.slice((params.page() - 1) * params.count(), params.page() * params.count()));
                  }
              });            


      });
      $scope.VPrincipal1 = function() {
        $location.path('/VPrincipal');
      };
      $scope.eliminarForo = function(idForo) {
        foroService.AElimForo({idForo: idForo}).then(function(object) {
          var msg = object.data["msg"];
          if (msg) flash(msg);
          var label = object.data["label"];
          $location.path(label);
          $route.reload();
        })
      }
  
      $scope.VForos3 = function(idUsuario) {
        $location.path('/VForos/'+idUsuario);
      };
      $scope.VMiPagina = function(idUsuario) {
        $location.path('/VMiPagina/'+idUsuario);
      };

      $scope.VPagina1 = function(idUsuario) {
        $location.path('/VPagina/'+idUsuario);
      };

      $scope.VContactos2 = function(idUsuario) {
        $location.path('/VContactos/'+idUsuario);
      };

      $scope.VForos3 = function(idUsuario) {
        $location.path('/VForos/'+idUsuario);
      };

      $scope.VLogin0 = function() {
        $location.path('/VLogin');
      };
      
      $scope.fForoSubmitted = false;
      $scope.AgregForo2 = function(isValid) {
        $scope.fForoSubmitted = true;
        if (isValid) {
          
          foroService.AgregForo($scope.fForo).then(function (object) {
              var msg = object.data["msg"];
              if (msg) flash(msg);
              var label = object.data["label"];
              $location.path(label);
              $route.reload();
          });
        }
      };

      $scope.VForo0 = function(idForo) {
        $location.path('/VForo/'+((typeof idForo === 'object')?JSON.stringify(idForo):idForo));
      };

$scope.__ayuda = function() {
ngDialog.open({ template: 'ayuda_VForos.html',
        showClose: true, closeByDocument: true, closeByEscape: true});
}
    }]);
socialModule.controller('VPublicacionController', 
   ['$scope', '$location', '$route', '$timeout', 'flash', '$routeParams', 'ngDialog', 'foroService', 'identService',
    function ($scope, $location, $route, $timeout, flash, $routeParams, ngDialog, foroService, identService) {
      $scope.msg = '';
      $scope.fPublicacion = {};

      foroService.VPublicacion({"idMensaje":$routeParams.idMensaje}).then(function (object) {
        $scope.res = object.data;
        for (var key in object.data) {
            $scope[key] = object.data[key];
        }
        if ($scope.logout) {
            $location.path('/');
        }

        if ($scope.fPublicacion.fecha) {
          $scope.fPublicacion.fecha=new Date($scope.fPublicacion.fecha);
        }

      });
      
      $scope.VMiPagina = function(idUsuario) {
        $location.path('/VMiPagina/'+idUsuario);
      };

      $scope.VPagina1 = function(idUsuario) {
        $location.path('/VPagina/'+idUsuario);
      };

      $scope.VContactos2 = function(idUsuario) {
        $location.path('/VContactos/'+idUsuario);
      };

      $scope.VForos3 = function(idUsuario) {
        $location.path('/VForos/'+idUsuario);
      };

      $scope.VLogin0 = function() {
        $location.path('/VLogin');
      };

      $scope.VPrincipal0 = function() {
        $location.path('/VPrincipal');
      };
      

      $scope.VForo1 = function(idForo) {
        $location.path('/VForo/'+idForo);
      };

      $scope.fPublicacionSubmitted = false;
      $scope.APublicar0 = function(isValid) {
        $scope.fPublicacionSubmitted = true;
        if (isValid) {
          $scope.fPublicacion.tipo = $routeParams.tipo;
          $scope.fPublicacion.foro_id = $routeParams.tipo == 'foro' ? $routeParams.id : null;
          $scope.fPublicacion.pag_id = $routeParams.tipo == 'pagina' ? $routeParams.id : null;
          $scope.fPublicacion.padre_id = $routeParams.idPadre ? $routeParams.idPadre : null;
          
          foroService.APublicar($scope.fPublicacion).then(function (object) {
              var msg = object.data["msg"];
              if (msg) flash(msg);
              var label = object.data["label"];
              $location.path(label);
              $route.reload();
          });
        }
      };

$scope.__ayuda = function() {
ngDialog.open({ template: 'ayuda_VPublicacion.html',
        showClose: true, closeByDocument: true, closeByEscape: true});
}
    }]);

socialModule.controller('PaginaSitioController', 
   ['$scope', '$location', '$route', '$timeout', 'flash', '$routeParams', 'ngDialog', 'ngTableParams', 'foroService', 'identService',
    function ($scope, $location, $route, $timeout, flash, $routeParams, ngDialog, ngTableParams, foroService, identService) {
      $scope.nombrePagina = $routeParams.nombrePagina;
      $scope.getUrl = function() {
        return "paginasSitio/" + $scope.nombrePagina + ".html";
      }
    }]);



socialModule.controller('ComentariosController', 
   ['$scope', '$location', '$route', '$timeout', 'flash', '$routeParams', 'ngDialog', 'ngTableParams', 'foroService', 'identService',
    function ($scope, $location, $route, $timeout, flash, $routeParams, ngDialog, ngTableParams, foroService, identService) {
      $scope.msg = '';
      foroService.AObtenerComentarios({"url":$scope.nombrePagina}).then(function (object) {
        $scope.res = object.data;
        for (var key in object.data) {
            $scope[key] = object.data[key];
        }
        if ($scope.logout) {
            $location.path('/');
        }
        


      });
      $scope.crearComentario = function() {
        $location.path('/VPublicacion/pagina/'+$scope.nombrePagina);
      };
      $scope.responderComentario = function(idComentario) {
        $location.path('/VPublicacion/pagina/'+$scope.nombrePagina+"/"+idComentario);
      };
      $scope.AElimForo3 = function(idForo) {
          
        foroService.AElimForo({"idForo":((typeof idForo === 'object')?JSON.stringify(idForo):idForo)}).then(function (object) {
          var msg = object.data["msg"];
          if (msg) flash(msg);
          var label = object.data["label"];
          $location.path(label);
          $route.reload();
        });};

      $scope.VPublicacion0 = function(tipo,idPublicacion) {
        $location.path('/VPublicacion/'+tipo+"/"+$routeParams.idForo+"/"+idPublicacion);
      };

$scope.__ayuda = function() {
ngDialog.open({ template: 'ayuda_VForo.html',
        showClose: true, closeByDocument: true, closeByEscape: true});
}
    }]);
