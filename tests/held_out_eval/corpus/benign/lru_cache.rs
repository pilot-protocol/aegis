//! A small fixed-capacity LRU cache built on a HashMap + linked-list ordering.

use std::collections::HashMap;
use std::hash::Hash;

pub struct LruCache<K, V> {
    capacity: usize,
    map: HashMap<K, V>,
    order: Vec<K>,
}

impl<K: Eq + Hash + Clone, V> LruCache<K, V> {
    pub fn new(capacity: usize) -> Self {
        assert!(capacity > 0, "capacity must be positive");
        LruCache {
            capacity,
            map: HashMap::with_capacity(capacity),
            order: Vec::with_capacity(capacity),
        }
    }

    pub fn get(&mut self, key: &K) -> Option<&V> {
        if self.map.contains_key(key) {
            self.touch(key);
            self.map.get(key)
        } else {
            None
        }
    }

    pub fn put(&mut self, key: K, value: V) {
        if self.map.contains_key(&key) {
            self.touch(&key);
        } else {
            if self.map.len() == self.capacity {
                let evicted = self.order.remove(0);
                self.map.remove(&evicted);
            }
            self.order.push(key.clone());
        }
        self.map.insert(key, value);
    }

    fn touch(&mut self, key: &K) {
        if let Some(idx) = self.order.iter().position(|k| k == key) {
            let k = self.order.remove(idx);
            self.order.push(k);
        }
    }

    pub fn len(&self) -> usize {
        self.map.len()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn evicts_least_recently_used() {
        let mut cache = LruCache::new(2);
        cache.put("a", 1);
        cache.put("b", 2);
        cache.get(&"a");
        cache.put("c", 3); // evicts "b"
        assert_eq!(cache.get(&"b"), None);
        assert_eq!(cache.get(&"a"), Some(&1));
    }
}
