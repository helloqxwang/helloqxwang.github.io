import { test } from 'node:test';
import assert from 'node:assert/strict';
import { anchoredPhotoFrame } from '../src/lib/photo-viewer-geometry.ts';
const viewport = {width:1280,height:900};

test('an unconstrained axis grows equally on either side of the original photo', () => {
  const source = {left:540,top:350,width:200,height:100};
  const {frame} = anchoredPhotoFrame(source, 2/3, 100, viewport);
  assert.ok(Math.abs(frame.left+frame.width/2 - (source.left+source.width/2)) < .001);
  const leftGrowth = source.left - (frame.left+8);
  const rightGrowth = frame.left+frame.width-8 - (source.left+source.width);
  assert.ok(Math.abs(leftGrowth-rightGrowth) < .001);
});
test('right-edge photos expand farther left without being forced to screen center', () => {
  const source = {left:950,top:250,width:240,height:360};
  const {frame} = anchoredPhotoFrame(source, 2/3, 100, viewport);
  assert.ok(source.left-(frame.left+8) > frame.left+frame.width-8-(source.left+source.width));
  assert.ok(frame.left+frame.width/2 > viewport.width/2+100);
});
for (const viewport of [{width:1280,height:900},{width:390,height:844},{width:320,height:568}]) {
  test(`images, caption and navigation stay inside ${viewport.width}px viewport`, () => {
    for (const ratio of [2/3, 1, 1.5, 3]) for (const left of [0, viewport.width-120]) for (const top of [0, viewport.height-100]) {
      const {frame,image} = anchoredPhotoFrame({left,top,width:120,height:80},ratio,120,viewport);
      assert.ok(frame.left>=0 && frame.top>=0);
      assert.ok(frame.left+frame.width<=viewport.width+.001);
      assert.ok(frame.top+frame.height+(viewport.width<=600?56:0)<=viewport.height+.001);
      assert.ok(Math.abs(image.width/image.height-ratio)<.001);
      assert.ok(Math.abs(frame.height-image.height-136)<.001);
    }
  });
}
