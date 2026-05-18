export function timeAgo(dateStr) {
    // Force UTC parsing si pas de timezone dans la string
    const normalized = /Z|[+-]\d{2}:\d{2}$/.test(dateStr) ? dateStr : dateStr + "Z"
    const diff = Math.max(0, Date.now() - new Date(normalized).getTime())
    const seconds = Math.floor(diff / 1000)
    if (seconds < 60) return "À l'instant"
    const minutes = Math.floor(seconds / 60)
    if (minutes < 60) return `Il y a ${minutes} min`
    const hours = Math.floor(minutes / 60)
    if (hours < 24) return `Il y a ${hours}h`
    const days = Math.floor(hours / 24)
    return `Il y a ${days} jour${days > 1 ? "s" : ""}`
}
