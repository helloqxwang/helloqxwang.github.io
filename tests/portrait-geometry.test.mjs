import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { portraitGeometry } from '../src/lib/portrait-geometry.ts';
const { portraits } = JSON.parse(readFileSync(new URL('../src/data/media.json', import.meta.url)));
for (const viewport of [{width:1280,height:900}, {width:390,height:844}, {width:320,height:568}]) {
  test(`portrait reveal preserves face scale and position at ${viewport.width}px`, () => {
    const source = {left:viewport.width > 860 ? 840 : (viewport.width-270)/2,top:150,width:270,height:337.5};
    for (const photo of portraits) {
      const g = portraitGeometry(source, photo, viewport);
      assert.equal(g.image.width, g.smallImage.width);
      assert.equal(g.image.height, g.smallImage.height);
      assert.ok(Math.abs(g.frame.left + g.image.left - (source.left + g.smallImage.left)) < .001);
      assert.ok(Math.abs(g.frame.top + g.image.top - (source.top + g.smallImage.top)) < .001);
      assert.ok(g.frame.left >= 24 && g.frame.top >= 24);
      assert.ok(g.frame.left + g.frame.width <= viewport.width - 24 + .001);
      assert.ok(g.frame.top + g.frame.height <= viewport.height - 24 + .001);
      const fit = portraitGeometry(source, photo, viewport, true);
      assert.equal(fit.frame.width, fit.image.width);
      assert.equal(fit.frame.height, fit.image.height);
      assert.ok(Math.abs(fit.image.width/fit.image.height - photo.width/photo.height) < .001);
    }
  });
}
