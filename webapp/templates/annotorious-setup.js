// annotorious-setup.js

import { AnnotoriousOpenSeadragon } from '@recogito/annotorious-openseadragon';
import '@recogito/annotorious-openseadragon/dist/annotorious-openseadragon.css';

window.onload = function() {
  const viewer = OpenSeadragon({
    id: "openseadragon",
    prefixUrl: "https://cdnjs.cloudflare.com/ajax/libs/openseadragon/3.0.0/images/",
    tileSources: "https://iiif.universiteitleiden.nl/iiif/2/hdl:1887.1%252Fitem:2013596",
    defaultZoomLevel: 1.0,
    visibilityRatio: 1,
    constrainDuringPan: true,
    gestureSettingsMouse: {
      scrollToZoom: true,
      clickToZoom: false
    }
  });

  viewer.addHandler("open", function() {
    const anno = AnnotoriousOpenSeadragon(viewer, {
      allowEmpty: true,
      drawingEnabled: true,
      formatter: function(annotation) {
        return {
          fill: '#ff0000',
          fillOpacity: 0.25,
          stroke: '#ff0000',
          strokeWidth: 2
        };
      }
    });

    anno.on('createAnnotation', (annotation) => {
      console.log('Annotation created:', annotation);
    });

    anno.on('updateAnnotation', (annotation, previous) => {
      console.log('Annotation updated:', annotation);
    });

    anno.on('deleteAnnotation', (annotation) => {
      console.log('Annotation deleted:', annotation);
    });
  });
}
