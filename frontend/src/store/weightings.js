import { defineStore } from 'pinia';


export const useWeightingsStore = defineStore('Weightings', {
    state: () => ({
        pageSize: 5,
        totalItems: 0,
        currPage: 1,
        offset: 0,
        totalPages: 0,
    }),
    getters: {
        getPageSize: state => state.pageSize,
        getTotalItems: state => state.totalItems,
        getCurrPage: state => state.currPage,
        getOffset: state => state.offset,
        getTotalPages: state => state.totalPages,
    },
    actions: {
        setPageSize(size) {
            this.pageSize = size;
        },
        setTotalItems(totalItems) {
            this.totalItems = totalItems;
        },
        setCurrPage(currPage) {
            this.currPage = currPage;
        },
        setOffset(offset) {
            this.offset = offset;
        },
        setTotalPages(totalPages) {
            this.totalPages = totalPages;
        }
    }
});