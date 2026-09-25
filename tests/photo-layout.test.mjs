import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { layoutPhotos } from '../src/lib/photo-layout.ts';
const { photos } = JSON.parse(readFileSync(new URL('../src/data/media.json', import.meta.url)));
for (const width of [292, 362, 560, 600, 601, 760, 980]) {
  test(`photo wall has no overlaps or overflow at ${width}px`, () => {
    const { items, height } = layoutPhotos(width, photos);
    assert.equal(items.length, 11);
    assert.equal(items[0].span, 4);
    assert.equal(items[0].top, 0);
    for (const rect of items) {
      assert.ok(rect.left >= 0 && rect.left + rect.width <= width + .01);
      assert.ok(rect.top >= 0 && rect.top + rect.height <= height + .01);
    }
    for (let a = 0; a < items.length; a++) for (let b = a + 1; b < items.length; b++) {
      const x = items[a], y = items[b];
      assert.ok(x.left + x.width <= y.left + .01 || y.left + y.width <= x.left + .01 ||
                x.top + x.height <= y.top + .01 || y.top + y.height <= x.top + .01);
    }
    // Every landscape gets two conventional columns; portraits stay one.
    photos.forEach((photo, index) => {
      assert.equal(items[index].span, photo.width >= photo.height ? 4 : 2);
    });
  });
}
test('a featured portrait gets a one-and-a-half-column width', () => {
  const { items } = layoutPhotos(980, [{ width: 400, height: 600, priority: 1 }, { width: 400, height: 600, priority: 0 }]);
  assert.equal(items[0].span, 3);
  assert.equal(items[1].span, 2);
  assert.ok(items[0].width > items[1].width);
});
test('empty gallery has zero height', () => assert.equal(layoutPhotos(980, []).height, 0));
