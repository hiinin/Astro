/**
 * Helpers e constantes para o módulo DONKI (Space Weather).
 */

const donkiList = (json) => (Array.isArray(json) ? json : (json.items ?? []))

export const DONKI_TABS = [
  { id: 'cme', label: 'CME', path: '/donki/cme', transform: donkiList },
  { id: 'cme-analysis', label: 'Análise CME', path: '/donki/cme-analysis', transform: donkiList },
  { id: 'flr', label: 'Erupções', path: '/donki/flr', transform: donkiList },
  { id: 'gst', label: 'Geomagnéticas', path: '/donki/gst', transform: donkiList },
  { id: 'ips', label: 'IPS', path: '/donki/ips', transform: donkiList },
  { id: 'sep', label: 'SEP', path: '/donki/sep', transform: donkiList },
  { id: 'rbe', label: 'RBE', path: '/donki/rbe', transform: donkiList },
  { id: 'hss', label: 'HSS', path: '/donki/hss', transform: donkiList },
  { id: 'wsa-enlil', label: 'WSA-Enlil', path: '/donki/wsa-enlil', transform: donkiList },
  { id: 'notifications', label: 'Notificações', path: '/donki/notifications', transform: donkiList },
]

export function donkiStart(item) {
  const t = item.cmeInputs?.[0]?.cmeStartTime ?? item.modelCompletionTime
    ?? item.beginTime ?? item.startTime ?? item.eventTime ?? item.messageIssueTime
    ?? item.associatedCMEStartTime ?? item.estimatedShockArrivalTime ?? item.submissionTime ?? item.peakTime
  return t?.split('T')[0] ?? '—'
}

export function donkiId(item, i) {
  return item.simulationID ?? item.activityID ?? item.gstID ?? item.flrID ?? item.cmeID ?? item.ipsID
    ?? item.notificationID ?? `#${i + 1}`
}

export function donkiNote(item) {
  if (item.note) return item.note
  if (item.messageBody) return item.messageBody
  if (item.messageSubject) return item.messageSubject
  const impact = item.impactList?.[0]
  if (impact) {
    const d = impact.arrivalTime?.split('T')[0]
    return d ? `${impact.location} · ${d}` : impact.location
  }
  if (item.estimatedShockArrivalTime) return `Choque ~ ${item.estimatedShockArrivalTime.split('T')[0]}`
  const kp = item.allKpIndex?.length ? Math.max(...item.allKpIndex.map((k) => k.kpIndex)) : null
  if (kp != null) return `Kp ${kp}`
  const wsaKp = [item.kp_180, item.kp_135, item.kp_90, item.kp_18].find((k) => k != null)
  if (wsaKp != null) return `Kp ${wsaKp}`
  if (item.classType) return `Classe ${item.classType}`
  const inst = item.instruments?.map((x) => x.displayName ?? x).filter(Boolean).join(', ')
  if (item.location && inst) return `${item.location} · ${inst}`
  if (item.location) return item.location
  if (inst) return inst
  if (item.catalog) return item.catalog
  const speed = item.cmeInputs?.[0]?.speed
  if (speed) return `CME ${Math.round(speed)} km/s`
  return '—'
}
