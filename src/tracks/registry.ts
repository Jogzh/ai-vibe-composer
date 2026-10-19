import { starter } from './starter.ts';

/** Register your own TrackDefinition here. */
export const trackRegistry = [starter];
export const defaultTrack = starter;

export function findTrack(id: string) {
  return trackRegistry.find(track => track.meta.id === id);
}
