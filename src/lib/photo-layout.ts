export type PhotoSize = { width: number; height: number; priority: number };
export type PhotoRect = { left: number; top: number; width: number; height: number; span: number };

/** Half-column skyline packing supports 1, 1.5, and 2-column prints without cropping. */
export function layoutPhotos(width: number, photos: PhotoSize[]) {
  const mobile = width <= 600;
  const columns = mobile ? 4 : 6;
  const gap = mobile ? 12 : 18;
  const border = mobile ? 10 : 16;
  const unit = (width - gap * (columns - 1)) / columns;
  const skyline = Array<number>(columns).fill(0);
  const items: PhotoRect[] = photos.map((photo) => {
    const span = photo.width >= photo.height ? 4 : photo.priority === 1 ? 3 : 2;
    let column = 0, top = Infinity;
    for (let start = 0; start <= columns - span; start++) {
      const candidate = Math.max(...skyline.slice(start, start + span));
      if (candidate < top - .01) { column = start; top = candidate; }
    }
    const tileWidth = unit * span + gap * (span - 1);
    const height = Math.ceil((tileWidth - border) * photo.height / photo.width + border);
    for (let i = column; i < column + span; i++) skyline[i] = top + height + gap;
    return { left: column * (unit + gap), top, width: tileWidth, height, span };
  });
  return { items, height: Math.max(0, ...skyline) - (items.length ? gap : 0) };
}
