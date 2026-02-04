<template>
  <div v-if="totalPages > 1" class="pagination">
    <div class="pagination-info">
      <p>
        Showing {{ startItem }}-{{ endItem }} of {{ totalCount }} properties
      </p>
    </div>

    <div class="pagination-controls">
      <!-- Previous Button -->
      <button
        class="pagination-btn"
        :disabled="!hasPreviousPage"
        @click="$emit('previous')"
        aria-label="Previous page"
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="m15 18-6-6 6-6"/>
        </svg>
      </button>

      <!-- Page Numbers -->
      <div class="page-numbers">
        <button
          v-for="page in displayPages"
          :key="page"
          :class="['page-btn', { active: page === currentPage, ellipsis: page === '...' }]"
          :disabled="page === '...'"
          @click="page !== '...' && $emit('goto', page)"
        >
          {{ page }}
        </button>
      </div>

      <!-- Next Button -->
      <button
        class="pagination-btn"
        :disabled="!hasNextPage"
        @click="$emit('next')"
        aria-label="Next page"
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="m9 18 6-6-6-6"/>
        </svg>
      </button>
    </div>

    <!-- Page Size Selector -->
    <div class="page-size-selector">
      <label>Per page:</label>
      <select :value="pageSize" @change="$emit('changePageSize', Number(($event.target as HTMLSelectElement).value))">
        <option :value="10">10</option>
        <option :value="20">20</option>
        <option :value="50">50</option>
        <option :value="100">100</option>
      </select>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

interface Props {
  currentPage: number;
  totalPages: number;
  totalCount: number;
  pageSize: number;
  hasNextPage: boolean;
  hasPreviousPage: boolean;
}

const props = defineProps<Props>();

defineEmits<{
  next: [];
  previous: [];
  goto: [page: number];
  changePageSize: [size: number];
}>();

const startItem = computed(() => {
  if (props.totalCount === 0) return 0;
  return (props.currentPage - 1) * props.pageSize + 1;
});

const endItem = computed(() => {
  const end = props.currentPage * props.pageSize;
  return Math.min(end, props.totalCount);
});

// Calculate which page numbers to display
const displayPages = computed(() => {
  const pages: (number | string)[] = [];
  const maxVisible = 7; // Maximum number of page buttons to show

  if (props.totalPages <= maxVisible) {
    // Show all pages if total is small
    for (let i = 1; i <= props.totalPages; i++) {
      pages.push(i);
    }
  } else {
    // Always show first page
    pages.push(1);

    if (props.currentPage > 3) {
      pages.push('...');
    }

    // Show pages around current page
    const start = Math.max(2, props.currentPage - 1);
    const end = Math.min(props.totalPages - 1, props.currentPage + 1);

    for (let i = start; i <= end; i++) {
      pages.push(i);
    }

    if (props.currentPage < props.totalPages - 2) {
      pages.push('...');
    }

    // Always show last page
    pages.push(props.totalPages);
  }

  return pages;
});
</script>

<style scoped>
.pagination {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1.5rem;
  padding: 1.5rem;
  margin-top: 2rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  flex-wrap: wrap;
}

.pagination-info p {
  color: #64748b;
  font-size: 0.9rem;
  margin: 0;
}

.pagination-controls {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.pagination-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border: 1px solid #e2e8f0;
  background: white;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  color: #475569;
}

.pagination-btn:hover:not(:disabled) {
  background: #f8fafc;
  border-color: #cbd5e1;
  color: #1e293b;
}

.pagination-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.page-numbers {
  display: flex;
  gap: 0.25rem;
}

.page-btn {
  min-width: 36px;
  height: 36px;
  padding: 0 0.5rem;
  border: 1px solid #e2e8f0;
  background: white;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  color: #475569;
  font-weight: 500;
  font-size: 0.9rem;
}

.page-btn:hover:not(:disabled):not(.active) {
  background: #f8fafc;
  border-color: #cbd5e1;
}

.page-btn.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-color: transparent;
}

.page-btn.ellipsis {
  border: none;
  cursor: default;
  color: #94a3b8;
}

.page-btn:disabled {
  cursor: not-allowed;
}

.page-size-selector {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.page-size-selector label {
  color: #64748b;
  font-size: 0.9rem;
}

.page-size-selector select {
  padding: 0.5rem;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  background: white;
  cursor: pointer;
  font-size: 0.9rem;
  color: #1e293b;
  transition: border-color 0.2s;
}

.page-size-selector select:hover {
  border-color: #cbd5e1;
}

.page-size-selector select:focus {
  outline: none;
  border-color: #667eea;
}

@media (max-width: 768px) {
  .pagination {
    flex-direction: column;
    gap: 1rem;
  }

  .pagination-info {
    width: 100%;
    text-align: center;
  }

  .page-size-selector {
    width: 100%;
    justify-content: center;
  }
}
</style>
