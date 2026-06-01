export function formatType(type) {
  const map = {
    internship: 'Praksa',
    education: 'Edukacija',
    scholarship: 'Stipendija'
  }
  return map[type] || 'Prilika'
}

export function formatStatus(status) {
  const map = {
    active: 'Aktivan',
    pending: 'Na čekanju',
    expired: 'Istekao',
    rejected: 'Odbijen',
    changes_requested: 'Potrebne izmjene'
  }
  return map[status] || 'Aktivan'
}

export function formatCompensation(value, currency) {
  if (value === null || value === undefined) return ''
  return `${value} ${currency || 'BAM'}`
}

export function mapAd(ad, companyName) {
  return {
    id: ad.id,
    title: ad.title,
    company: companyName,
    description: ad.description,
    tags: [ad.field, ad.location].filter(Boolean),
    typeLabel: formatType(ad.type),
    compensation: formatCompensation(ad.compensation, ad.currency),
    statusLabel: formatStatus(ad.status),
    statusKey: ad.status,
    typeKey: ad.type,
    location: ad.location || 'Nije navedeno',
    duration: ad.duration_months ? `${ad.duration_months} mjeseci` : null,
    field: ad.field || ''
  }
}