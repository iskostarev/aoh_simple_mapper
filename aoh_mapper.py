#!/usr/bin/env python

import argparse
import sys
from PIL import Image


TILE_SIZE = 100


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', required=True, type=argparse.FileType('r'))
    parser.add_argument('-o', '--output', required=True, type=argparse.FileType('wb'))
    return parser.parse_args()


def parse_input(input_file):
    target = None
    map_xy = None
    fragments = []

    for line in input_file:
        line = line.strip().split()
        if not line:
            continue

        if line[0] == ':target':
            if target is not None:
                raise RuntimeError(':target must be unique')
            if len(line) != 5:
                raise RuntimeError(':target must take 4 arguments')
            txmin, tymin, txmax, tymax = map(int, line[1:])
            if txmin >= txmax or tymin >= tymax:
                raise RuntimeError(':target arguments must be in order: x_min, y_min, x_max, y_max')

            target = {
                'x_min': txmin,
                'y_min': tymin,
                'x_max': txmax,
                'y_max': tymax,
            }
        elif line[0] == ':mapxy':
            if len(line) != 3:
                raise RuntimeError(':mapxy must take 2 arguments')
            map_xy = (int(line[1]), int(line[2]))
        elif line[0].startswith(':'):
            raise RuntimeError(f'Invalid command {line[0]}')
        else:
            if len(line) != 3:
                raise RuntimeError('Map fragment must take 2 arguments')

            if map_xy is None:
                raise RuntimeError('Expected :mapxy before fragments')

            fragments.append({
                'path': line[0],
                'center_x': int(line[1]),
                'center_y': int(line[2]),
                'map_x': map_xy[0],
                'map_y': map_xy[1],
            })

    if target is None:
        raise RuntimeError('Expected :target')

    return target, fragments


def read_tiles(tiles, fragment):
    with Image.open(fragment['path']) as image:
        left = fragment['map_x']
        right = left + TILE_SIZE*3
        top = fragment['map_y']
        bottom = top + TILE_SIZE*3
        image = image.crop((left, top, right, bottom))
        cx, cy = fragment['center_x'], fragment['center_y']
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                x = cx + dx
                y = cy + dy
                tile_left = (dx + 1)*TILE_SIZE
                tile_right = tile_left + TILE_SIZE
                tile_top = (dy + 1)*TILE_SIZE
                tile_bottom = tile_top + TILE_SIZE
                tiles[x, y] = image.crop((tile_left, tile_top, tile_right, tile_bottom))


def validate_tiles(tiles, target):
    missing = []
    for x in range(target['x_min'], target['x_max']+1):
        for y in range(target['y_min'], target['y_max']+1):
            if (x, y) not in tiles:
                missing.append((x, y))

    if missing:
        raise RuntimeError(f'The following tiles are missing: {missing}')


def merge_map(tiles, target):
    width = (target['x_max'] - target['x_min'] + 1)*TILE_SIZE
    height = (target['y_max'] - target['y_min'] + 1)*TILE_SIZE
    result = Image.new('RGB', (width, height))

    for x in range(target['x_min'], target['x_max']+1):
        for y in range(target['y_min'], target['y_max']+1):
            im_x = (x - target['x_min'])*TILE_SIZE
            im_y = (y - target['y_min'])*TILE_SIZE
            result.paste(tiles[x, y], (im_x, im_y))

    return result


def main():
    args = parse_args()
    target, fragments = parse_input(args.input)

    tiles = {}
    for fragment in fragments:
        read_tiles(tiles, fragment)

    validate_tiles(tiles, target)
    merged_map = merge_map(tiles, target)
    merged_map.save(args.output)


if __name__ == '__main__':
    main()
