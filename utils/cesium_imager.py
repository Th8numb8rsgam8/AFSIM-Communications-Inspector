from flask import make_response
from dash import html, Input, Output

class CesiumJSGlobe:

   online_external_css = ['https://cesium.com/downloads/cesiumjs/releases/1.129/Build/Cesium/Widgets/widgets.css']
   online_external_scripts = [{'src':'https://cesium.com/downloads/cesiumjs/releases/1.129/Build/Cesium/Cesium.js'}]
   offline_external_scripts = [{'src': '/assets/Cesium.js'}]
   offline_external_stylesheets = ['/static/widgets.css']

   cesium_element_id = "cesium-graph"
   cesium_startup = '''
   function(id) {
      // const osm = Cesium.OpenStreetMapImageryProvider({
      //    url: "https://tile.openstreetmap.org/"
      // });
      // const viewer = new Cesium.Viewer(id, {
      //    baseLayerPicker: false,
      //    geocoder: false,
      // });
      // viewer.imageryLayers.addImageryProvider(osm);

      // const viewer = new Cesium.Viewer(id, {
      //    baseLayer: Cesium.ImageryLayer.fromProviderAsync(
      //       Cesium.TileMapServiceImageryProvider.fromUrl(
      //          Cesium.buildModuleUrl("Assets/Textures/NaturalEarthII"),
      //       ),
      //    ),
      //    baseLayerPicker: false,
      //    geocoder: false,
      // });

      const viewer = new Cesium.Viewer(id, {
         baseLayerPicker: false,
         geocoder: false
      });
      const world_jpg = "http://localhost:8050/world";
      const imageryLayer = new Cesium.ImageryLayer(
         new Cesium.SingleTileImageryProvider({
            url: world_jpg
         })
      );
      viewer.imageryLayers.add(imageryLayer);

      return true;
   }
   '''

   @classmethod
   def add_cesium_element(cls):

      return html.Div(id=cls.cesium_element_id)


   @classmethod
   def add_cesium_feature(cls, app):

      app.config.external_scripts.extend(cls.offline_external_scripts)
      app.config.external_stylesheets.extend(cls.offline_external_stylesheets)

      app.clientside_callback(
         cls.cesium_startup,
         Output(cls.cesium_element_id, 'data-done'),
         Input(cls.cesium_element_id, 'id')
      )

      @app.server.route("/world")
      def get_world_image():

         with open("C:\\GIT_REPOS\\comms_inspector\\earth_data\world.jpg", 'rb') as f:
            response = make_response(f.read())
            response.headers["Content-Type"] = 'text/plain'
            response.headers["Access-Control-Allow-Origin"] = '*'
            return response
