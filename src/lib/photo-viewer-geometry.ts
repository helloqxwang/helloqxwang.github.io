export type PhotoRect = { left: number; top: number; width: number; height: number };
const clamp = (value: number, low: number, high: number) => Math.max(low, Math.min(high, value));

/** Grow about the selected photograph, redistributing space at viewport edges. */
export function anchoredPhotoFrame(anchor: PhotoRect, ratio: number, captionHeight: number, viewport: {width: number; height: number}) {
  const compact = viewport.width <= 600;
  const side = compact ? 10 : 64;
  const top = compact ? 18 : 32;
  const bottom = compact ? 74 : 32;
  const maxWidth = Math.min(1100, viewport.width - 2 * side - 16);
  const maxHeight = Math.max(1, viewport.height - top - bottom - captionHeight - 16);
  const width = Math.max(1, Math.min(maxWidth, maxHeight * ratio));
  const height = width / ratio;
  const frameWidth = width + 16, frameHeight = height + captionHeight + 16;
  return {
    image: { width, height },
    frame: {
      left: clamp(anchor.left + anchor.width / 2 - frameWidth / 2, side, viewport.width - side - frameWidth),
      top: clamp(anchor.top + anchor.height / 2 - height / 2 - 8, top, viewport.height - bottom - frameHeight),
      width: frameWidth, height: frameHeight,
    },
  };
}
