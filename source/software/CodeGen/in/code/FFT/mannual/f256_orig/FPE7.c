#include "header.h"


// **** Fire function declaration **** //
static inline void butterfly_sharecoe(int i0, int i1, int *o0, int *o1, int W) {
asm ("ADDMULSRA1 %[A0], %[b0], %[w0], %[a0]\n\t"
     "SUBMULSRA1 %[B0], %[b0], %[w0], %[a0]\n\t"
     : [A0]"=&r"(*o0), [B0]"=&r"(*o1)
     : [b0]"r"(i1), [w0]"i"(W), [a0]"r"(i0)
      );
}

// **** Main function **** //
void FPE7PE0() {

  // **** Variable declaration **** //
	int T1792_i0;
	int T1792_i1;
	int T1792_o0;
	int T1792_o1;
	int T1792_W;

	int T1793_i0;
	int T1793_i1;
	int T1793_o0;
	int T1793_o1;
	int T1793_W;

	int T1794_i0;
	int T1794_i1;
	int T1794_o0;
	int T1794_o1;
	int T1794_W;

	int T1795_i0;
	int T1795_i1;
	int T1795_o0;
	int T1795_o1;
	int T1795_W;

	int T1796_i0;
	int T1796_i1;
	int T1796_o0;
	int T1796_o1;
	int T1796_W;

	int T1797_i0;
	int T1797_i1;
	int T1797_o0;
	int T1797_o1;
	int T1797_W;

	int T1798_i0;
	int T1798_i1;
	int T1798_o0;
	int T1798_o1;
	int T1798_W;

	int T1799_i0;
	int T1799_i1;
	int T1799_o0;
	int T1799_o1;
	int T1799_W;

	int T1800_i0;
	int T1800_i1;
	int T1800_o0;
	int T1800_o1;
	int T1800_W;

	int T1801_i0;
	int T1801_i1;
	int T1801_o0;
	int T1801_o1;
	int T1801_W;

	int T1802_i0;
	int T1802_i1;
	int T1802_o0;
	int T1802_o1;
	int T1802_W;

	int T1803_i0;
	int T1803_i1;
	int T1803_o0;
	int T1803_o1;
	int T1803_W;

	int T1804_i0;
	int T1804_i1;
	int T1804_o0;
	int T1804_o1;
	int T1804_W;

	int T1805_i0;
	int T1805_i1;
	int T1805_o0;
	int T1805_o1;
	int T1805_W;

	int T1806_i0;
	int T1806_i1;
	int T1806_o0;
	int T1806_o1;
	int T1806_W;

	int T1807_i0;
	int T1807_i1;
	int T1807_o0;
	int T1807_o1;
	int T1807_W;

	int T1808_i0;
	int T1808_i1;
	int T1808_o0;
	int T1808_o1;
	int T1808_W;

	int T1809_i0;
	int T1809_i1;
	int T1809_o0;
	int T1809_o1;
	int T1809_W;

	int T1810_i0;
	int T1810_i1;
	int T1810_o0;
	int T1810_o1;
	int T1810_W;

	int T1811_i0;
	int T1811_i1;
	int T1811_o0;
	int T1811_o1;
	int T1811_W;

	int T1812_i0;
	int T1812_i1;
	int T1812_o0;
	int T1812_o1;
	int T1812_W;

	int T1813_i0;
	int T1813_i1;
	int T1813_o0;
	int T1813_o1;
	int T1813_W;

	int T1814_i0;
	int T1814_i1;
	int T1814_o0;
	int T1814_o1;
	int T1814_W;

	int T1815_i0;
	int T1815_i1;
	int T1815_o0;
	int T1815_o1;
	int T1815_W;

	int T1816_i0;
	int T1816_i1;
	int T1816_o0;
	int T1816_o1;
	int T1816_W;

	int T1817_i0;
	int T1817_i1;
	int T1817_o0;
	int T1817_o1;
	int T1817_W;

	int T1818_i0;
	int T1818_i1;
	int T1818_o0;
	int T1818_o1;
	int T1818_W;

	int T1819_i0;
	int T1819_i1;
	int T1819_o0;
	int T1819_o1;
	int T1819_W;

	int T1820_i0;
	int T1820_i1;
	int T1820_o0;
	int T1820_o1;
	int T1820_W;

	int T1821_i0;
	int T1821_i1;
	int T1821_o0;
	int T1821_o1;
	int T1821_W;

	int T1822_i0;
	int T1822_i1;
	int T1822_o0;
	int T1822_o1;
	int T1822_W;

	int T1823_i0;
	int T1823_i1;
	int T1823_o0;
	int T1823_o1;
	int T1823_W;

	int T1824_i0;
	int T1824_i1;
	int T1824_o0;
	int T1824_o1;
	int T1824_W;

	int T1825_i0;
	int T1825_i1;
	int T1825_o0;
	int T1825_o1;
	int T1825_W;

	int T1826_i0;
	int T1826_i1;
	int T1826_o0;
	int T1826_o1;
	int T1826_W;

	int T1827_i0;
	int T1827_i1;
	int T1827_o0;
	int T1827_o1;
	int T1827_W;

	int T1828_i0;
	int T1828_i1;
	int T1828_o0;
	int T1828_o1;
	int T1828_W;

	int T1829_i0;
	int T1829_i1;
	int T1829_o0;
	int T1829_o1;
	int T1829_W;

	int T1830_i0;
	int T1830_i1;
	int T1830_o0;
	int T1830_o1;
	int T1830_W;

	int T1831_i0;
	int T1831_i1;
	int T1831_o0;
	int T1831_o1;
	int T1831_W;

	int T1832_i0;
	int T1832_i1;
	int T1832_o0;
	int T1832_o1;
	int T1832_W;

	int T1833_i0;
	int T1833_i1;
	int T1833_o0;
	int T1833_o1;
	int T1833_W;

	int T1834_i0;
	int T1834_i1;
	int T1834_o0;
	int T1834_o1;
	int T1834_W;

	int T1835_i0;
	int T1835_i1;
	int T1835_o0;
	int T1835_o1;
	int T1835_W;

	int T1836_i0;
	int T1836_i1;
	int T1836_o0;
	int T1836_o1;
	int T1836_W;

	int T1837_i0;
	int T1837_i1;
	int T1837_o0;
	int T1837_o1;
	int T1837_W;

	int T1838_i0;
	int T1838_i1;
	int T1838_o0;
	int T1838_o1;
	int T1838_W;

	int T1839_i0;
	int T1839_i1;
	int T1839_o0;
	int T1839_o1;
	int T1839_W;

	int T1840_i0;
	int T1840_i1;
	int T1840_o0;
	int T1840_o1;
	int T1840_W;

	int T1841_i0;
	int T1841_i1;
	int T1841_o0;
	int T1841_o1;
	int T1841_W;

	int T1842_i0;
	int T1842_i1;
	int T1842_o0;
	int T1842_o1;
	int T1842_W;

	int T1843_i0;
	int T1843_i1;
	int T1843_o0;
	int T1843_o1;
	int T1843_W;

	int T1844_i0;
	int T1844_i1;
	int T1844_o0;
	int T1844_o1;
	int T1844_W;

	int T1845_i0;
	int T1845_i1;
	int T1845_o0;
	int T1845_o1;
	int T1845_W;

	int T1846_i0;
	int T1846_i1;
	int T1846_o0;
	int T1846_o1;
	int T1846_W;

	int T1847_i0;
	int T1847_i1;
	int T1847_o0;
	int T1847_o1;
	int T1847_W;

	int T1848_i0;
	int T1848_i1;
	int T1848_o0;
	int T1848_o1;
	int T1848_W;

	int T1849_i0;
	int T1849_i1;
	int T1849_o0;
	int T1849_o1;
	int T1849_W;

	int T1850_i0;
	int T1850_i1;
	int T1850_o0;
	int T1850_o1;
	int T1850_W;

	int T1851_i0;
	int T1851_i1;
	int T1851_o0;
	int T1851_o1;
	int T1851_W;

	int T1852_i0;
	int T1852_i1;
	int T1852_o0;
	int T1852_o1;
	int T1852_W;

	int T1853_i0;
	int T1853_i1;
	int T1853_o0;
	int T1853_o1;
	int T1853_W;

	int T1854_i0;
	int T1854_i1;
	int T1854_o0;
	int T1854_o1;
	int T1854_W;

	int T1855_i0;
	int T1855_i1;
	int T1855_o0;
	int T1855_o1;
	int T1855_W;

	int T1856_i0;
	int T1856_i1;
	int T1856_o0;
	int T1856_o1;
	int T1856_W;

	int T1857_i0;
	int T1857_i1;
	int T1857_o0;
	int T1857_o1;
	int T1857_W;

	int T1858_i0;
	int T1858_i1;
	int T1858_o0;
	int T1858_o1;
	int T1858_W;

	int T1859_i0;
	int T1859_i1;
	int T1859_o0;
	int T1859_o1;
	int T1859_W;

	int T1860_i0;
	int T1860_i1;
	int T1860_o0;
	int T1860_o1;
	int T1860_W;

	int T1861_i0;
	int T1861_i1;
	int T1861_o0;
	int T1861_o1;
	int T1861_W;

	int T1862_i0;
	int T1862_i1;
	int T1862_o0;
	int T1862_o1;
	int T1862_W;

	int T1863_i0;
	int T1863_i1;
	int T1863_o0;
	int T1863_o1;
	int T1863_W;

	int T1864_i0;
	int T1864_i1;
	int T1864_o0;
	int T1864_o1;
	int T1864_W;

	int T1865_i0;
	int T1865_i1;
	int T1865_o0;
	int T1865_o1;
	int T1865_W;

	int T1866_i0;
	int T1866_i1;
	int T1866_o0;
	int T1866_o1;
	int T1866_W;

	int T1867_i0;
	int T1867_i1;
	int T1867_o0;
	int T1867_o1;
	int T1867_W;

	int T1868_i0;
	int T1868_i1;
	int T1868_o0;
	int T1868_o1;
	int T1868_W;

	int T1869_i0;
	int T1869_i1;
	int T1869_o0;
	int T1869_o1;
	int T1869_W;

	int T1870_i0;
	int T1870_i1;
	int T1870_o0;
	int T1870_o1;
	int T1870_W;

	int T1871_i0;
	int T1871_i1;
	int T1871_o0;
	int T1871_o1;
	int T1871_W;

	int T1872_i0;
	int T1872_i1;
	int T1872_o0;
	int T1872_o1;
	int T1872_W;

	int T1873_i0;
	int T1873_i1;
	int T1873_o0;
	int T1873_o1;
	int T1873_W;

	int T1874_i0;
	int T1874_i1;
	int T1874_o0;
	int T1874_o1;
	int T1874_W;

	int T1875_i0;
	int T1875_i1;
	int T1875_o0;
	int T1875_o1;
	int T1875_W;

	int T1876_i0;
	int T1876_i1;
	int T1876_o0;
	int T1876_o1;
	int T1876_W;

	int T1877_i0;
	int T1877_i1;
	int T1877_o0;
	int T1877_o1;
	int T1877_W;

	int T1878_i0;
	int T1878_i1;
	int T1878_o0;
	int T1878_o1;
	int T1878_W;

	int T1879_i0;
	int T1879_i1;
	int T1879_o0;
	int T1879_o1;
	int T1879_W;

	int T1880_i0;
	int T1880_i1;
	int T1880_o0;
	int T1880_o1;
	int T1880_W;

	int T1881_i0;
	int T1881_i1;
	int T1881_o0;
	int T1881_o1;
	int T1881_W;

	int T1882_i0;
	int T1882_i1;
	int T1882_o0;
	int T1882_o1;
	int T1882_W;

	int T1883_i0;
	int T1883_i1;
	int T1883_o0;
	int T1883_o1;
	int T1883_W;

	int T1884_i0;
	int T1884_i1;
	int T1884_o0;
	int T1884_o1;
	int T1884_W;

	int T1885_i0;
	int T1885_i1;
	int T1885_o0;
	int T1885_o1;
	int T1885_W;

	int T1886_i0;
	int T1886_i1;
	int T1886_o0;
	int T1886_o1;
	int T1886_W;

	int T1887_i0;
	int T1887_i1;
	int T1887_o0;
	int T1887_o1;
	int T1887_W;

	int T1888_i0;
	int T1888_i1;
	int T1888_o0;
	int T1888_o1;
	int T1888_W;

	int T1889_i0;
	int T1889_i1;
	int T1889_o0;
	int T1889_o1;
	int T1889_W;

	int T1890_i0;
	int T1890_i1;
	int T1890_o0;
	int T1890_o1;
	int T1890_W;

	int T1891_i0;
	int T1891_i1;
	int T1891_o0;
	int T1891_o1;
	int T1891_W;

	int T1892_i0;
	int T1892_i1;
	int T1892_o0;
	int T1892_o1;
	int T1892_W;

	int T1893_i0;
	int T1893_i1;
	int T1893_o0;
	int T1893_o1;
	int T1893_W;

	int T1894_i0;
	int T1894_i1;
	int T1894_o0;
	int T1894_o1;
	int T1894_W;

	int T1895_i0;
	int T1895_i1;
	int T1895_o0;
	int T1895_o1;
	int T1895_W;

	int T1896_i0;
	int T1896_i1;
	int T1896_o0;
	int T1896_o1;
	int T1896_W;

	int T1897_i0;
	int T1897_i1;
	int T1897_o0;
	int T1897_o1;
	int T1897_W;

	int T1898_i0;
	int T1898_i1;
	int T1898_o0;
	int T1898_o1;
	int T1898_W;

	int T1899_i0;
	int T1899_i1;
	int T1899_o0;
	int T1899_o1;
	int T1899_W;

	int T1900_i0;
	int T1900_i1;
	int T1900_o0;
	int T1900_o1;
	int T1900_W;

	int T1901_i0;
	int T1901_i1;
	int T1901_o0;
	int T1901_o1;
	int T1901_W;

	int T1902_i0;
	int T1902_i1;
	int T1902_o0;
	int T1902_o1;
	int T1902_W;

	int T1903_i0;
	int T1903_i1;
	int T1903_o0;
	int T1903_o1;
	int T1903_W;

	int T1904_i0;
	int T1904_i1;
	int T1904_o0;
	int T1904_o1;
	int T1904_W;

	int T1905_i0;
	int T1905_i1;
	int T1905_o0;
	int T1905_o1;
	int T1905_W;

	int T1906_i0;
	int T1906_i1;
	int T1906_o0;
	int T1906_o1;
	int T1906_W;

	int T1907_i0;
	int T1907_i1;
	int T1907_o0;
	int T1907_o1;
	int T1907_W;

	int T1908_i0;
	int T1908_i1;
	int T1908_o0;
	int T1908_o1;
	int T1908_W;

	int T1909_i0;
	int T1909_i1;
	int T1909_o0;
	int T1909_o1;
	int T1909_W;

	int T1910_i0;
	int T1910_i1;
	int T1910_o0;
	int T1910_o1;
	int T1910_W;

	int T1911_i0;
	int T1911_i1;
	int T1911_o0;
	int T1911_o1;
	int T1911_W;

	int T1912_i0;
	int T1912_i1;
	int T1912_o0;
	int T1912_o1;
	int T1912_W;

	int T1913_i0;
	int T1913_i1;
	int T1913_o0;
	int T1913_o1;
	int T1913_W;

	int T1914_i0;
	int T1914_i1;
	int T1914_o0;
	int T1914_o1;
	int T1914_W;

	int T1915_i0;
	int T1915_i1;
	int T1915_o0;
	int T1915_o1;
	int T1915_W;

	int T1916_i0;
	int T1916_i1;
	int T1916_o0;
	int T1916_o1;
	int T1916_W;

	int T1917_i0;
	int T1917_i1;
	int T1917_o0;
	int T1917_o1;
	int T1917_W;

	int T1918_i0;
	int T1918_i1;
	int T1918_o0;
	int T1918_o1;
	int T1918_W;

	int T1919_i0;
	int T1919_i1;
	int T1919_o0;
	int T1919_o1;
	int T1919_W;

	int T1920_i0;
	int T1920_i1;
	int T1920_o0;
	int T1920_o1;
	int T1920_W;

	int T1921_i0;
	int T1921_i1;
	int T1921_o0;
	int T1921_o1;
	int T1921_W;

	int T1922_i0;
	int T1922_i1;
	int T1922_o0;
	int T1922_o1;
	int T1922_W;

	int T1923_i0;
	int T1923_i1;
	int T1923_o0;
	int T1923_o1;
	int T1923_W;

	int T1924_i0;
	int T1924_i1;
	int T1924_o0;
	int T1924_o1;
	int T1924_W;

	int T1925_i0;
	int T1925_i1;
	int T1925_o0;
	int T1925_o1;
	int T1925_W;

	int T1926_i0;
	int T1926_i1;
	int T1926_o0;
	int T1926_o1;
	int T1926_W;

	int T1927_i0;
	int T1927_i1;
	int T1927_o0;
	int T1927_o1;
	int T1927_W;

	int T1928_i0;
	int T1928_i1;
	int T1928_o0;
	int T1928_o1;
	int T1928_W;

	int T1929_i0;
	int T1929_i1;
	int T1929_o0;
	int T1929_o1;
	int T1929_W;

	int T1930_i0;
	int T1930_i1;
	int T1930_o0;
	int T1930_o1;
	int T1930_W;

	int T1931_i0;
	int T1931_i1;
	int T1931_o0;
	int T1931_o1;
	int T1931_W;

	int T1932_i0;
	int T1932_i1;
	int T1932_o0;
	int T1932_o1;
	int T1932_W;

	int T1933_i0;
	int T1933_i1;
	int T1933_o0;
	int T1933_o1;
	int T1933_W;

	int T1934_i0;
	int T1934_i1;
	int T1934_o0;
	int T1934_o1;
	int T1934_W;

	int T1935_i0;
	int T1935_i1;
	int T1935_o0;
	int T1935_o1;
	int T1935_W;

	int T1936_i0;
	int T1936_i1;
	int T1936_o0;
	int T1936_o1;
	int T1936_W;

	int T1937_i0;
	int T1937_i1;
	int T1937_o0;
	int T1937_o1;
	int T1937_W;

	int T1938_i0;
	int T1938_i1;
	int T1938_o0;
	int T1938_o1;
	int T1938_W;

	int T1939_i0;
	int T1939_i1;
	int T1939_o0;
	int T1939_o1;
	int T1939_W;

	int T1940_i0;
	int T1940_i1;
	int T1940_o0;
	int T1940_o1;
	int T1940_W;

	int T1941_i0;
	int T1941_i1;
	int T1941_o0;
	int T1941_o1;
	int T1941_W;

	int T1942_i0;
	int T1942_i1;
	int T1942_o0;
	int T1942_o1;
	int T1942_W;

	int T1943_i0;
	int T1943_i1;
	int T1943_o0;
	int T1943_o1;
	int T1943_W;

	int T1944_i0;
	int T1944_i1;
	int T1944_o0;
	int T1944_o1;
	int T1944_W;

	int T1945_i0;
	int T1945_i1;
	int T1945_o0;
	int T1945_o1;
	int T1945_W;

	int T1946_i0;
	int T1946_i1;
	int T1946_o0;
	int T1946_o1;
	int T1946_W;

	int T1947_i0;
	int T1947_i1;
	int T1947_o0;
	int T1947_o1;
	int T1947_W;

	int T1948_i0;
	int T1948_i1;
	int T1948_o0;
	int T1948_o1;
	int T1948_W;

	int T1949_i0;
	int T1949_i1;
	int T1949_o0;
	int T1949_o1;
	int T1949_W;

	int T1950_i0;
	int T1950_i1;
	int T1950_o0;
	int T1950_o1;
	int T1950_W;

	int T1951_i0;
	int T1951_i1;
	int T1951_o0;
	int T1951_o1;
	int T1951_W;

	int T1952_i0;
	int T1952_i1;
	int T1952_o0;
	int T1952_o1;
	int T1952_W;

	int T1953_i0;
	int T1953_i1;
	int T1953_o0;
	int T1953_o1;
	int T1953_W;

	int T1954_i0;
	int T1954_i1;
	int T1954_o0;
	int T1954_o1;
	int T1954_W;

	int T1955_i0;
	int T1955_i1;
	int T1955_o0;
	int T1955_o1;
	int T1955_W;

	int T1956_i0;
	int T1956_i1;
	int T1956_o0;
	int T1956_o1;
	int T1956_W;

	int T1957_i0;
	int T1957_i1;
	int T1957_o0;
	int T1957_o1;
	int T1957_W;

	int T1958_i0;
	int T1958_i1;
	int T1958_o0;
	int T1958_o1;
	int T1958_W;

	int T1959_i0;
	int T1959_i1;
	int T1959_o0;
	int T1959_o1;
	int T1959_W;

	int T1960_i0;
	int T1960_i1;
	int T1960_o0;
	int T1960_o1;
	int T1960_W;

	int T1961_i0;
	int T1961_i1;
	int T1961_o0;
	int T1961_o1;
	int T1961_W;

	int T1962_i0;
	int T1962_i1;
	int T1962_o0;
	int T1962_o1;
	int T1962_W;

	int T1963_i0;
	int T1963_i1;
	int T1963_o0;
	int T1963_o1;
	int T1963_W;

	int T1964_i0;
	int T1964_i1;
	int T1964_o0;
	int T1964_o1;
	int T1964_W;

	int T1965_i0;
	int T1965_i1;
	int T1965_o0;
	int T1965_o1;
	int T1965_W;

	int T1966_i0;
	int T1966_i1;
	int T1966_o0;
	int T1966_o1;
	int T1966_W;

	int T1967_i0;
	int T1967_i1;
	int T1967_o0;
	int T1967_o1;
	int T1967_W;

	int T1968_i0;
	int T1968_i1;
	int T1968_o0;
	int T1968_o1;
	int T1968_W;

	int T1969_i0;
	int T1969_i1;
	int T1969_o0;
	int T1969_o1;
	int T1969_W;

	int T1970_i0;
	int T1970_i1;
	int T1970_o0;
	int T1970_o1;
	int T1970_W;

	int T1971_i0;
	int T1971_i1;
	int T1971_o0;
	int T1971_o1;
	int T1971_W;

	int T1972_i0;
	int T1972_i1;
	int T1972_o0;
	int T1972_o1;
	int T1972_W;

	int T1973_i0;
	int T1973_i1;
	int T1973_o0;
	int T1973_o1;
	int T1973_W;

	int T1974_i0;
	int T1974_i1;
	int T1974_o0;
	int T1974_o1;
	int T1974_W;

	int T1975_i0;
	int T1975_i1;
	int T1975_o0;
	int T1975_o1;
	int T1975_W;

	int T1976_i0;
	int T1976_i1;
	int T1976_o0;
	int T1976_o1;
	int T1976_W;

	int T1977_i0;
	int T1977_i1;
	int T1977_o0;
	int T1977_o1;
	int T1977_W;

	int T1978_i0;
	int T1978_i1;
	int T1978_o0;
	int T1978_o1;
	int T1978_W;

	int T1979_i0;
	int T1979_i1;
	int T1979_o0;
	int T1979_o1;
	int T1979_W;

	int T1980_i0;
	int T1980_i1;
	int T1980_o0;
	int T1980_o1;
	int T1980_W;

	int T1981_i0;
	int T1981_i1;
	int T1981_o0;
	int T1981_o1;
	int T1981_W;

	int T1982_i0;
	int T1982_i1;
	int T1982_o0;
	int T1982_o1;
	int T1982_W;

	int T1983_i0;
	int T1983_i1;
	int T1983_o0;
	int T1983_o1;
	int T1983_W;

	int T1984_i0;
	int T1984_i1;
	int T1984_o0;
	int T1984_o1;
	int T1984_W;

	int T1985_i0;
	int T1985_i1;
	int T1985_o0;
	int T1985_o1;
	int T1985_W;

	int T1986_i0;
	int T1986_i1;
	int T1986_o0;
	int T1986_o1;
	int T1986_W;

	int T1987_i0;
	int T1987_i1;
	int T1987_o0;
	int T1987_o1;
	int T1987_W;

	int T1988_i0;
	int T1988_i1;
	int T1988_o0;
	int T1988_o1;
	int T1988_W;

	int T1989_i0;
	int T1989_i1;
	int T1989_o0;
	int T1989_o1;
	int T1989_W;

	int T1990_i0;
	int T1990_i1;
	int T1990_o0;
	int T1990_o1;
	int T1990_W;

	int T1991_i0;
	int T1991_i1;
	int T1991_o0;
	int T1991_o1;
	int T1991_W;

	int T1992_i0;
	int T1992_i1;
	int T1992_o0;
	int T1992_o1;
	int T1992_W;

	int T1993_i0;
	int T1993_i1;
	int T1993_o0;
	int T1993_o1;
	int T1993_W;

	int T1994_i0;
	int T1994_i1;
	int T1994_o0;
	int T1994_o1;
	int T1994_W;

	int T1995_i0;
	int T1995_i1;
	int T1995_o0;
	int T1995_o1;
	int T1995_W;

	int T1996_i0;
	int T1996_i1;
	int T1996_o0;
	int T1996_o1;
	int T1996_W;

	int T1997_i0;
	int T1997_i1;
	int T1997_o0;
	int T1997_o1;
	int T1997_W;

	int T1998_i0;
	int T1998_i1;
	int T1998_o0;
	int T1998_o1;
	int T1998_W;

	int T1999_i0;
	int T1999_i1;
	int T1999_o0;
	int T1999_o1;
	int T1999_W;

	int T2000_i0;
	int T2000_i1;
	int T2000_o0;
	int T2000_o1;
	int T2000_W;

	int T2001_i0;
	int T2001_i1;
	int T2001_o0;
	int T2001_o1;
	int T2001_W;

	int T2002_i0;
	int T2002_i1;
	int T2002_o0;
	int T2002_o1;
	int T2002_W;

	int T2003_i0;
	int T2003_i1;
	int T2003_o0;
	int T2003_o1;
	int T2003_W;

	int T2004_i0;
	int T2004_i1;
	int T2004_o0;
	int T2004_o1;
	int T2004_W;

	int T2005_i0;
	int T2005_i1;
	int T2005_o0;
	int T2005_o1;
	int T2005_W;

	int T2006_i0;
	int T2006_i1;
	int T2006_o0;
	int T2006_o1;
	int T2006_W;

	int T2007_i0;
	int T2007_i1;
	int T2007_o0;
	int T2007_o1;
	int T2007_W;

	int T2008_i0;
	int T2008_i1;
	int T2008_o0;
	int T2008_o1;
	int T2008_W;

	int T2009_i0;
	int T2009_i1;
	int T2009_o0;
	int T2009_o1;
	int T2009_W;

	int T2010_i0;
	int T2010_i1;
	int T2010_o0;
	int T2010_o1;
	int T2010_W;

	int T2011_i0;
	int T2011_i1;
	int T2011_o0;
	int T2011_o1;
	int T2011_W;

	int T2012_i0;
	int T2012_i1;
	int T2012_o0;
	int T2012_o1;
	int T2012_W;

	int T2013_i0;
	int T2013_i1;
	int T2013_o0;
	int T2013_o1;
	int T2013_W;

	int T2014_i0;
	int T2014_i1;
	int T2014_o0;
	int T2014_o1;
	int T2014_W;

	int T2015_i0;
	int T2015_i1;
	int T2015_o0;
	int T2015_o1;
	int T2015_W;

	int T2016_i0;
	int T2016_i1;
	int T2016_o0;
	int T2016_o1;
	int T2016_W;

	int T2017_i0;
	int T2017_i1;
	int T2017_o0;
	int T2017_o1;
	int T2017_W;

	int T2018_i0;
	int T2018_i1;
	int T2018_o0;
	int T2018_o1;
	int T2018_W;

	int T2019_i0;
	int T2019_i1;
	int T2019_o0;
	int T2019_o1;
	int T2019_W;

	int T2020_i0;
	int T2020_i1;
	int T2020_o0;
	int T2020_o1;
	int T2020_W;

	int T2021_i0;
	int T2021_i1;
	int T2021_o0;
	int T2021_o1;
	int T2021_W;

	int T2022_i0;
	int T2022_i1;
	int T2022_o0;
	int T2022_o1;
	int T2022_W;

	int T2023_i0;
	int T2023_i1;
	int T2023_o0;
	int T2023_o1;
	int T2023_W;

	int T2024_i0;
	int T2024_i1;
	int T2024_o0;
	int T2024_o1;
	int T2024_W;

	int T2025_i0;
	int T2025_i1;
	int T2025_o0;
	int T2025_o1;
	int T2025_W;

	int T2026_i0;
	int T2026_i1;
	int T2026_o0;
	int T2026_o1;
	int T2026_W;

	int T2027_i0;
	int T2027_i1;
	int T2027_o0;
	int T2027_o1;
	int T2027_W;

	int T2028_i0;
	int T2028_i1;
	int T2028_o0;
	int T2028_o1;
	int T2028_W;

	int T2029_i0;
	int T2029_i1;
	int T2029_o0;
	int T2029_o1;
	int T2029_W;

	int T2030_i0;
	int T2030_i1;
	int T2030_o0;
	int T2030_o1;
	int T2030_W;

	int T2031_i0;
	int T2031_i1;
	int T2031_o0;
	int T2031_o1;
	int T2031_W;

	int T2032_i0;
	int T2032_i1;
	int T2032_o0;
	int T2032_o1;
	int T2032_W;

	int T2033_i0;
	int T2033_i1;
	int T2033_o0;
	int T2033_o1;
	int T2033_W;

	int T2034_i0;
	int T2034_i1;
	int T2034_o0;
	int T2034_o1;
	int T2034_W;

	int T2035_i0;
	int T2035_i1;
	int T2035_o0;
	int T2035_o1;
	int T2035_W;

	int T2036_i0;
	int T2036_i1;
	int T2036_o0;
	int T2036_o1;
	int T2036_W;

	int T2037_i0;
	int T2037_i1;
	int T2037_o0;
	int T2037_o1;
	int T2037_W;

	int T2038_i0;
	int T2038_i1;
	int T2038_o0;
	int T2038_o1;
	int T2038_W;

	int T2039_i0;
	int T2039_i1;
	int T2039_o0;
	int T2039_o1;
	int T2039_W;

	int T2040_i0;
	int T2040_i1;
	int T2040_o0;
	int T2040_o1;
	int T2040_W;

	int T2041_i0;
	int T2041_i1;
	int T2041_o0;
	int T2041_o1;
	int T2041_W;

	int T2042_i0;
	int T2042_i1;
	int T2042_o0;
	int T2042_o1;
	int T2042_W;

	int T2043_i0;
	int T2043_i1;
	int T2043_o0;
	int T2043_o1;
	int T2043_W;

	int T2044_i0;
	int T2044_i1;
	int T2044_o0;
	int T2044_o1;
	int T2044_W;

	int T2045_i0;
	int T2045_i1;
	int T2045_o0;
	int T2045_o1;
	int T2045_W;

	int T2046_i0;
	int T2046_i1;
	int T2046_o0;
	int T2046_o1;
	int T2046_W;

	int T2047_i0;
	int T2047_i1;
	int T2047_o0;
	int T2047_o1;
	int T2047_W;


  // **** Parameter initialisation **** //
T1792_W = 16384;
T1793_W = -26329093;
T1794_W = -52674580;
T1795_W = -78954540;
T1796_W = -105234511;
T1797_W = -131448955;
T1798_W = -157532337;
T1799_W = -183550193;
T1800_W = -209436987;
T1801_W = -235258254;
T1802_W = -260882923;
T1803_W = -286376529;
T1804_W = -311673537;
T1805_W = -336773947;
T1806_W = -361743294;
T1807_W = -386450506;
T1808_W = -410895583;
T1809_W = -435078526;
T1810_W = -459064869;
T1811_W = -482723541;
T1812_W = -506120079;
T1813_W = -529254480;
T1814_W = -551995675;
T1815_W = -574409198;
T1816_W = -596495049;
T1817_W = -618253229;
T1818_W = -639618200;
T1819_W = -660589964;
T1820_W = -681168519;
T1821_W = -701353866;
T1822_W = -721080468;
T1823_W = -740348326;
T1824_W = -759222975;
T1825_W = -777638879;
T1826_W = -795596037;
T1827_W = -813028914;
T1828_W = -830003046;
T1829_W = -846452896;
T1830_W = -862444000;
T1831_W = -877845286;
T1832_W = -892787826;
T1833_W = -907140547;
T1834_W = -920968985;
T1835_W = -934273140;
T1836_W = -946921941;
T1837_W = -959111994;
T1838_W = -970646691;
T1839_W = -981591569;
T1840_W = -992012162;
T1841_W = -1001777399;
T1842_W = -1010952816;
T1843_W = -1019538413;
T1844_W = -1027534188;
T1845_W = -1034874606;
T1846_W = -1041559667;
T1847_W = -1047654906;
T1848_W = -1053094788;
T1849_W = -1057944847;
T1850_W = -1062139548;
T1851_W = -1065678890;
T1852_W = -1068562874;
T1853_W = -1070857035;
T1854_W = -1072430300;
T1855_W = -1073413742;
T1856_W = -1073741824;
T1857_W = -1073414546;
T1858_W = -1072431908;
T1859_W = -1070859445;
T1860_W = -1068566086;
T1861_W = -1065682902;
T1862_W = -1062144356;
T1863_W = -1057950449;
T1864_W = -1053101180;
T1865_W = -1047662086;
T1866_W = -1041567629;
T1867_W = -1034883346;
T1868_W = -1027543700;
T1869_W = -1019548691;
T1870_W = -1010963856;
T1871_W = -1001789193;
T1872_W = -992024702;
T1873_W = -981604847;
T1874_W = -970660701;
T1875_W = -959126726;
T1876_W = -946937387;
T1877_W = -934289292;
T1878_W = -920985831;
T1879_W = -907158077;
T1880_W = -892806030;
T1881_W = -877864154;
T1882_W = -862463520;
T1883_W = -846473056;
T1884_W = -830023834;
T1885_W = -813050318;
T1886_W = -795618043;
T1887_W = -777661473;
T1888_W = -759246145;
T1889_W = -740372058;
T1890_W = -721104748;
T1891_W = -701378678;
T1892_W = -681193849;
T1893_W = -660615796;
T1894_W = -639644520;
T1895_W = -618280019;
T1896_W = -596522295;
T1897_W = -574436882;
T1898_W = -552023781;
T1899_W = -529282992;
T1900_W = -506148977;
T1901_W = -482752811;
T1902_W = -459094491;
T1903_W = -435108482;
T1904_W = -410925857;
T1905_W = -386481078;
T1906_W = -361774146;
T1907_W = -336805061;
T1908_W = -311704895;
T1909_W = -286408111;
T1910_W = -260914709;
T1911_W = -235290226;
T1912_W = -209469125;
T1913_W = -183582479;
T1914_W = -157564751;
T1915_W = -131481477;
T1916_W = -105267121;
T1917_W = -78987220;
T1918_W = -52707308;
T1919_W = -26361851;
T1920_W = 16384;
T1921_W = -26329093;
T1922_W = -52674580;
T1923_W = -78954540;
T1924_W = -105234511;
T1925_W = -131448955;
T1926_W = -157532337;
T1927_W = -183550193;
T1928_W = -209436987;
T1929_W = -235258254;
T1930_W = -260882923;
T1931_W = -286376529;
T1932_W = -311673537;
T1933_W = -336773947;
T1934_W = -361743294;
T1935_W = -386450506;
T1936_W = -410895583;
T1937_W = -435078526;
T1938_W = -459064869;
T1939_W = -482723541;
T1940_W = -506120079;
T1941_W = -529254480;
T1942_W = -551995675;
T1943_W = -574409198;
T1944_W = -596495049;
T1945_W = -618253229;
T1946_W = -639618200;
T1947_W = -660589964;
T1948_W = -681168519;
T1949_W = -701353866;
T1950_W = -721080468;
T1951_W = -740348326;
T1952_W = -759222975;
T1953_W = -777638879;
T1954_W = -795596037;
T1955_W = -813028914;
T1956_W = -830003046;
T1957_W = -846452896;
T1958_W = -862444000;
T1959_W = -877845286;
T1960_W = -892787826;
T1961_W = -907140547;
T1962_W = -920968985;
T1963_W = -934273140;
T1964_W = -946921941;
T1965_W = -959111994;
T1966_W = -970646691;
T1967_W = -981591569;
T1968_W = -992012162;
T1969_W = -1001777399;
T1970_W = -1010952816;
T1971_W = -1019538413;
T1972_W = -1027534188;
T1973_W = -1034874606;
T1974_W = -1041559667;
T1975_W = -1047654906;
T1976_W = -1053094788;
T1977_W = -1057944847;
T1978_W = -1062139548;
T1979_W = -1065678890;
T1980_W = -1068562874;
T1981_W = -1070857035;
T1982_W = -1072430300;
T1983_W = -1073413742;
T1984_W = -1073741824;
T1985_W = -1073414546;
T1986_W = -1072431908;
T1987_W = -1070859445;
T1988_W = -1068566086;
T1989_W = -1065682902;
T1990_W = -1062144356;
T1991_W = -1057950449;
T1992_W = -1053101180;
T1993_W = -1047662086;
T1994_W = -1041567629;
T1995_W = -1034883346;
T1996_W = -1027543700;
T1997_W = -1019548691;
T1998_W = -1010963856;
T1999_W = -1001789193;
T2000_W = -992024702;
T2001_W = -981604847;
T2002_W = -970660701;
T2003_W = -959126726;
T2004_W = -946937387;
T2005_W = -934289292;
T2006_W = -920985831;
T2007_W = -907158077;
T2008_W = -892806030;
T2009_W = -877864154;
T2010_W = -862463520;
T2011_W = -846473056;
T2012_W = -830023834;
T2013_W = -813050318;
T2014_W = -795618043;
T2015_W = -777661473;
T2016_W = -759246145;
T2017_W = -740372058;
T2018_W = -721104748;
T2019_W = -701378678;
T2020_W = -681193849;
T2021_W = -660615796;
T2022_W = -639644520;
T2023_W = -618280019;
T2024_W = -596522295;
T2025_W = -574436882;
T2026_W = -552023781;
T2027_W = -529282992;
T2028_W = -506148977;
T2029_W = -482752811;
T2030_W = -459094491;
T2031_W = -435108482;
T2032_W = -410925857;
T2033_W = -386481078;
T2034_W = -361774146;
T2035_W = -336805061;
T2036_W = -311704895;
T2037_W = -286408111;
T2038_W = -260914709;
T2039_W = -235290226;
T2040_W = -209469125;
T2041_W = -183582479;
T2042_W = -157564751;
T2043_W = -131481477;
T2044_W = -105267121;
T2045_W = -78987220;
T2046_W = -52707308;
T2047_W = -26361851;

  // **** Code body **** //

	GET_FIFO(T1792_i0, 0);
	GET_FIFO(T1792_i1, 2);
	Butterfly(T1792_i0, T1792_i1, &T1792_o0, &T1792_o1, T1792_W);
	PUT_FIFO(T1792_o0, 0);
	PUT_FIFO(T1792_o1, 1);

	GET_FIFO(T1793_i0, 0);
	GET_FIFO(T1793_i1, 2);
	Butterfly(T1793_i0, T1793_i1, &T1793_o0, &T1793_o1, T1793_W);
	PUT_FIFO(T1793_o0, 0);
	PUT_FIFO(T1793_o1, 1);

	GET_FIFO(T1794_i0, 0);
	GET_FIFO(T1794_i1, 2);
	Butterfly(T1794_i0, T1794_i1, &T1794_o0, &T1794_o1, T1794_W);
	PUT_FIFO(T1794_o0, 0);
	PUT_FIFO(T1794_o1, 1);

	GET_FIFO(T1795_i0, 0);
	GET_FIFO(T1795_i1, 2);
	Butterfly(T1795_i0, T1795_i1, &T1795_o0, &T1795_o1, T1795_W);
	PUT_FIFO(T1795_o0, 0);
	PUT_FIFO(T1795_o1, 1);

	GET_FIFO(T1796_i0, 0);
	GET_FIFO(T1796_i1, 2);
	Butterfly(T1796_i0, T1796_i1, &T1796_o0, &T1796_o1, T1796_W);
	PUT_FIFO(T1796_o0, 0);
	PUT_FIFO(T1796_o1, 1);

	GET_FIFO(T1797_i0, 0);
	GET_FIFO(T1797_i1, 2);
	Butterfly(T1797_i0, T1797_i1, &T1797_o0, &T1797_o1, T1797_W);
	PUT_FIFO(T1797_o0, 0);
	PUT_FIFO(T1797_o1, 1);

	GET_FIFO(T1798_i0, 0);
	GET_FIFO(T1798_i1, 2);
	Butterfly(T1798_i0, T1798_i1, &T1798_o0, &T1798_o1, T1798_W);
	PUT_FIFO(T1798_o0, 0);
	PUT_FIFO(T1798_o1, 1);

	GET_FIFO(T1799_i0, 0);
	GET_FIFO(T1799_i1, 2);
	Butterfly(T1799_i0, T1799_i1, &T1799_o0, &T1799_o1, T1799_W);
	PUT_FIFO(T1799_o0, 0);
	PUT_FIFO(T1799_o1, 1);

	GET_FIFO(T1800_i0, 0);
	GET_FIFO(T1800_i1, 2);
	Butterfly(T1800_i0, T1800_i1, &T1800_o0, &T1800_o1, T1800_W);
	PUT_FIFO(T1800_o0, 0);
	PUT_FIFO(T1800_o1, 1);

	GET_FIFO(T1801_i0, 0);
	GET_FIFO(T1801_i1, 2);
	Butterfly(T1801_i0, T1801_i1, &T1801_o0, &T1801_o1, T1801_W);
	PUT_FIFO(T1801_o0, 0);
	PUT_FIFO(T1801_o1, 1);

	GET_FIFO(T1802_i0, 0);
	GET_FIFO(T1802_i1, 2);
	Butterfly(T1802_i0, T1802_i1, &T1802_o0, &T1802_o1, T1802_W);
	PUT_FIFO(T1802_o0, 0);
	PUT_FIFO(T1802_o1, 1);

	GET_FIFO(T1803_i0, 0);
	GET_FIFO(T1803_i1, 2);
	Butterfly(T1803_i0, T1803_i1, &T1803_o0, &T1803_o1, T1803_W);
	PUT_FIFO(T1803_o0, 0);
	PUT_FIFO(T1803_o1, 1);

	GET_FIFO(T1804_i0, 0);
	GET_FIFO(T1804_i1, 2);
	Butterfly(T1804_i0, T1804_i1, &T1804_o0, &T1804_o1, T1804_W);
	PUT_FIFO(T1804_o0, 0);
	PUT_FIFO(T1804_o1, 1);

	GET_FIFO(T1805_i0, 0);
	GET_FIFO(T1805_i1, 2);
	Butterfly(T1805_i0, T1805_i1, &T1805_o0, &T1805_o1, T1805_W);
	PUT_FIFO(T1805_o0, 0);
	PUT_FIFO(T1805_o1, 1);

	GET_FIFO(T1806_i0, 0);
	GET_FIFO(T1806_i1, 2);
	Butterfly(T1806_i0, T1806_i1, &T1806_o0, &T1806_o1, T1806_W);
	PUT_FIFO(T1806_o0, 0);
	PUT_FIFO(T1806_o1, 1);

	GET_FIFO(T1807_i0, 0);
	GET_FIFO(T1807_i1, 2);
	Butterfly(T1807_i0, T1807_i1, &T1807_o0, &T1807_o1, T1807_W);
	PUT_FIFO(T1807_o0, 0);
	PUT_FIFO(T1807_o1, 1);

	GET_FIFO(T1808_i0, 0);
	GET_FIFO(T1808_i1, 2);
	Butterfly(T1808_i0, T1808_i1, &T1808_o0, &T1808_o1, T1808_W);
	PUT_FIFO(T1808_o0, 0);
	PUT_FIFO(T1808_o1, 1);

	GET_FIFO(T1809_i0, 0);
	GET_FIFO(T1809_i1, 2);
	Butterfly(T1809_i0, T1809_i1, &T1809_o0, &T1809_o1, T1809_W);
	PUT_FIFO(T1809_o0, 0);
	PUT_FIFO(T1809_o1, 1);

	GET_FIFO(T1810_i0, 0);
	GET_FIFO(T1810_i1, 2);
	Butterfly(T1810_i0, T1810_i1, &T1810_o0, &T1810_o1, T1810_W);
	PUT_FIFO(T1810_o0, 0);
	PUT_FIFO(T1810_o1, 1);

	GET_FIFO(T1811_i0, 0);
	GET_FIFO(T1811_i1, 2);
	Butterfly(T1811_i0, T1811_i1, &T1811_o0, &T1811_o1, T1811_W);
	PUT_FIFO(T1811_o0, 0);
	PUT_FIFO(T1811_o1, 1);

	GET_FIFO(T1812_i0, 0);
	GET_FIFO(T1812_i1, 2);
	Butterfly(T1812_i0, T1812_i1, &T1812_o0, &T1812_o1, T1812_W);
	PUT_FIFO(T1812_o0, 0);
	PUT_FIFO(T1812_o1, 1);

	GET_FIFO(T1813_i0, 0);
	GET_FIFO(T1813_i1, 2);
	Butterfly(T1813_i0, T1813_i1, &T1813_o0, &T1813_o1, T1813_W);
	PUT_FIFO(T1813_o0, 0);
	PUT_FIFO(T1813_o1, 1);

	GET_FIFO(T1814_i0, 0);
	GET_FIFO(T1814_i1, 2);
	Butterfly(T1814_i0, T1814_i1, &T1814_o0, &T1814_o1, T1814_W);
	PUT_FIFO(T1814_o0, 0);
	PUT_FIFO(T1814_o1, 1);

	GET_FIFO(T1815_i0, 0);
	GET_FIFO(T1815_i1, 2);
	Butterfly(T1815_i0, T1815_i1, &T1815_o0, &T1815_o1, T1815_W);
	PUT_FIFO(T1815_o0, 0);
	PUT_FIFO(T1815_o1, 1);

	GET_FIFO(T1816_i0, 0);
	GET_FIFO(T1816_i1, 2);
	Butterfly(T1816_i0, T1816_i1, &T1816_o0, &T1816_o1, T1816_W);
	PUT_FIFO(T1816_o0, 0);
	PUT_FIFO(T1816_o1, 1);

	GET_FIFO(T1817_i0, 0);
	GET_FIFO(T1817_i1, 2);
	Butterfly(T1817_i0, T1817_i1, &T1817_o0, &T1817_o1, T1817_W);
	PUT_FIFO(T1817_o0, 0);
	PUT_FIFO(T1817_o1, 1);

	GET_FIFO(T1818_i0, 0);
	GET_FIFO(T1818_i1, 2);
	Butterfly(T1818_i0, T1818_i1, &T1818_o0, &T1818_o1, T1818_W);
	PUT_FIFO(T1818_o0, 0);
	PUT_FIFO(T1818_o1, 1);

	GET_FIFO(T1819_i0, 0);
	GET_FIFO(T1819_i1, 2);
	Butterfly(T1819_i0, T1819_i1, &T1819_o0, &T1819_o1, T1819_W);
	PUT_FIFO(T1819_o0, 0);
	PUT_FIFO(T1819_o1, 1);

	GET_FIFO(T1820_i0, 0);
	GET_FIFO(T1820_i1, 2);
	Butterfly(T1820_i0, T1820_i1, &T1820_o0, &T1820_o1, T1820_W);
	PUT_FIFO(T1820_o0, 0);
	PUT_FIFO(T1820_o1, 1);

	GET_FIFO(T1821_i0, 0);
	GET_FIFO(T1821_i1, 2);
	Butterfly(T1821_i0, T1821_i1, &T1821_o0, &T1821_o1, T1821_W);
	PUT_FIFO(T1821_o0, 0);
	PUT_FIFO(T1821_o1, 1);

	GET_FIFO(T1822_i0, 0);
	GET_FIFO(T1822_i1, 2);
	Butterfly(T1822_i0, T1822_i1, &T1822_o0, &T1822_o1, T1822_W);
	PUT_FIFO(T1822_o0, 0);
	PUT_FIFO(T1822_o1, 1);

	GET_FIFO(T1823_i0, 0);
	GET_FIFO(T1823_i1, 2);
	Butterfly(T1823_i0, T1823_i1, &T1823_o0, &T1823_o1, T1823_W);
	PUT_FIFO(T1823_o0, 0);
	PUT_FIFO(T1823_o1, 1);

	GET_FIFO(T1824_i0, 0);
	GET_FIFO(T1824_i1, 2);
	Butterfly(T1824_i0, T1824_i1, &T1824_o0, &T1824_o1, T1824_W);
	PUT_FIFO(T1824_o0, 0);
	PUT_FIFO(T1824_o1, 1);

	GET_FIFO(T1825_i0, 0);
	GET_FIFO(T1825_i1, 2);
	Butterfly(T1825_i0, T1825_i1, &T1825_o0, &T1825_o1, T1825_W);
	PUT_FIFO(T1825_o0, 0);
	PUT_FIFO(T1825_o1, 1);

	GET_FIFO(T1826_i0, 0);
	GET_FIFO(T1826_i1, 2);
	Butterfly(T1826_i0, T1826_i1, &T1826_o0, &T1826_o1, T1826_W);
	PUT_FIFO(T1826_o0, 0);
	PUT_FIFO(T1826_o1, 1);

	GET_FIFO(T1827_i0, 0);
	GET_FIFO(T1827_i1, 2);
	Butterfly(T1827_i0, T1827_i1, &T1827_o0, &T1827_o1, T1827_W);
	PUT_FIFO(T1827_o0, 0);
	PUT_FIFO(T1827_o1, 1);

	GET_FIFO(T1828_i0, 0);
	GET_FIFO(T1828_i1, 2);
	Butterfly(T1828_i0, T1828_i1, &T1828_o0, &T1828_o1, T1828_W);
	PUT_FIFO(T1828_o0, 0);
	PUT_FIFO(T1828_o1, 1);

	GET_FIFO(T1829_i0, 0);
	GET_FIFO(T1829_i1, 2);
	Butterfly(T1829_i0, T1829_i1, &T1829_o0, &T1829_o1, T1829_W);
	PUT_FIFO(T1829_o0, 0);
	PUT_FIFO(T1829_o1, 1);

	GET_FIFO(T1830_i0, 0);
	GET_FIFO(T1830_i1, 2);
	Butterfly(T1830_i0, T1830_i1, &T1830_o0, &T1830_o1, T1830_W);
	PUT_FIFO(T1830_o0, 0);
	PUT_FIFO(T1830_o1, 1);

	GET_FIFO(T1831_i0, 0);
	GET_FIFO(T1831_i1, 2);
	Butterfly(T1831_i0, T1831_i1, &T1831_o0, &T1831_o1, T1831_W);
	PUT_FIFO(T1831_o0, 0);
	PUT_FIFO(T1831_o1, 1);

	GET_FIFO(T1832_i0, 0);
	GET_FIFO(T1832_i1, 2);
	Butterfly(T1832_i0, T1832_i1, &T1832_o0, &T1832_o1, T1832_W);
	PUT_FIFO(T1832_o0, 0);
	PUT_FIFO(T1832_o1, 1);

	GET_FIFO(T1833_i0, 0);
	GET_FIFO(T1833_i1, 2);
	Butterfly(T1833_i0, T1833_i1, &T1833_o0, &T1833_o1, T1833_W);
	PUT_FIFO(T1833_o0, 0);
	PUT_FIFO(T1833_o1, 1);

	GET_FIFO(T1834_i0, 0);
	GET_FIFO(T1834_i1, 2);
	Butterfly(T1834_i0, T1834_i1, &T1834_o0, &T1834_o1, T1834_W);
	PUT_FIFO(T1834_o0, 0);
	PUT_FIFO(T1834_o1, 1);

	GET_FIFO(T1835_i0, 0);
	GET_FIFO(T1835_i1, 2);
	Butterfly(T1835_i0, T1835_i1, &T1835_o0, &T1835_o1, T1835_W);
	PUT_FIFO(T1835_o0, 0);
	PUT_FIFO(T1835_o1, 1);

	GET_FIFO(T1836_i0, 0);
	GET_FIFO(T1836_i1, 2);
	Butterfly(T1836_i0, T1836_i1, &T1836_o0, &T1836_o1, T1836_W);
	PUT_FIFO(T1836_o0, 0);
	PUT_FIFO(T1836_o1, 1);

	GET_FIFO(T1837_i0, 0);
	GET_FIFO(T1837_i1, 2);
	Butterfly(T1837_i0, T1837_i1, &T1837_o0, &T1837_o1, T1837_W);
	PUT_FIFO(T1837_o0, 0);
	PUT_FIFO(T1837_o1, 1);

	GET_FIFO(T1838_i0, 0);
	GET_FIFO(T1838_i1, 2);
	Butterfly(T1838_i0, T1838_i1, &T1838_o0, &T1838_o1, T1838_W);
	PUT_FIFO(T1838_o0, 0);
	PUT_FIFO(T1838_o1, 1);

	GET_FIFO(T1839_i0, 0);
	GET_FIFO(T1839_i1, 2);
	Butterfly(T1839_i0, T1839_i1, &T1839_o0, &T1839_o1, T1839_W);
	PUT_FIFO(T1839_o0, 0);
	PUT_FIFO(T1839_o1, 1);

	GET_FIFO(T1840_i0, 0);
	GET_FIFO(T1840_i1, 2);
	Butterfly(T1840_i0, T1840_i1, &T1840_o0, &T1840_o1, T1840_W);
	PUT_FIFO(T1840_o0, 0);
	PUT_FIFO(T1840_o1, 1);

	GET_FIFO(T1841_i0, 0);
	GET_FIFO(T1841_i1, 2);
	Butterfly(T1841_i0, T1841_i1, &T1841_o0, &T1841_o1, T1841_W);
	PUT_FIFO(T1841_o0, 0);
	PUT_FIFO(T1841_o1, 1);

	GET_FIFO(T1842_i0, 0);
	GET_FIFO(T1842_i1, 2);
	Butterfly(T1842_i0, T1842_i1, &T1842_o0, &T1842_o1, T1842_W);
	PUT_FIFO(T1842_o0, 0);
	PUT_FIFO(T1842_o1, 1);

	GET_FIFO(T1843_i0, 0);
	GET_FIFO(T1843_i1, 2);
	Butterfly(T1843_i0, T1843_i1, &T1843_o0, &T1843_o1, T1843_W);
	PUT_FIFO(T1843_o0, 0);
	PUT_FIFO(T1843_o1, 1);

	GET_FIFO(T1844_i0, 0);
	GET_FIFO(T1844_i1, 2);
	Butterfly(T1844_i0, T1844_i1, &T1844_o0, &T1844_o1, T1844_W);
	PUT_FIFO(T1844_o0, 0);
	PUT_FIFO(T1844_o1, 1);

	GET_FIFO(T1845_i0, 0);
	GET_FIFO(T1845_i1, 2);
	Butterfly(T1845_i0, T1845_i1, &T1845_o0, &T1845_o1, T1845_W);
	PUT_FIFO(T1845_o0, 0);
	PUT_FIFO(T1845_o1, 1);

	GET_FIFO(T1846_i0, 0);
	GET_FIFO(T1846_i1, 2);
	Butterfly(T1846_i0, T1846_i1, &T1846_o0, &T1846_o1, T1846_W);
	PUT_FIFO(T1846_o0, 0);
	PUT_FIFO(T1846_o1, 1);

	GET_FIFO(T1847_i0, 0);
	GET_FIFO(T1847_i1, 2);
	Butterfly(T1847_i0, T1847_i1, &T1847_o0, &T1847_o1, T1847_W);
	PUT_FIFO(T1847_o0, 0);
	PUT_FIFO(T1847_o1, 1);

	GET_FIFO(T1848_i0, 0);
	GET_FIFO(T1848_i1, 2);
	Butterfly(T1848_i0, T1848_i1, &T1848_o0, &T1848_o1, T1848_W);
	PUT_FIFO(T1848_o0, 0);
	PUT_FIFO(T1848_o1, 1);

	GET_FIFO(T1849_i0, 0);
	GET_FIFO(T1849_i1, 2);
	Butterfly(T1849_i0, T1849_i1, &T1849_o0, &T1849_o1, T1849_W);
	PUT_FIFO(T1849_o0, 0);
	PUT_FIFO(T1849_o1, 1);

	GET_FIFO(T1850_i0, 0);
	GET_FIFO(T1850_i1, 2);
	Butterfly(T1850_i0, T1850_i1, &T1850_o0, &T1850_o1, T1850_W);
	PUT_FIFO(T1850_o0, 0);
	PUT_FIFO(T1850_o1, 1);

	GET_FIFO(T1851_i0, 0);
	GET_FIFO(T1851_i1, 2);
	Butterfly(T1851_i0, T1851_i1, &T1851_o0, &T1851_o1, T1851_W);
	PUT_FIFO(T1851_o0, 0);
	PUT_FIFO(T1851_o1, 1);

	GET_FIFO(T1852_i0, 0);
	GET_FIFO(T1852_i1, 2);
	Butterfly(T1852_i0, T1852_i1, &T1852_o0, &T1852_o1, T1852_W);
	PUT_FIFO(T1852_o0, 0);
	PUT_FIFO(T1852_o1, 1);

	GET_FIFO(T1853_i0, 0);
	GET_FIFO(T1853_i1, 2);
	Butterfly(T1853_i0, T1853_i1, &T1853_o0, &T1853_o1, T1853_W);
	PUT_FIFO(T1853_o0, 0);
	PUT_FIFO(T1853_o1, 1);

	GET_FIFO(T1854_i0, 0);
	GET_FIFO(T1854_i1, 2);
	Butterfly(T1854_i0, T1854_i1, &T1854_o0, &T1854_o1, T1854_W);
	PUT_FIFO(T1854_o0, 0);
	PUT_FIFO(T1854_o1, 1);

	GET_FIFO(T1855_i0, 0);
	GET_FIFO(T1855_i1, 2);
	Butterfly(T1855_i0, T1855_i1, &T1855_o0, &T1855_o1, T1855_W);
	PUT_FIFO(T1855_o0, 0);
	PUT_FIFO(T1855_o1, 1);

	GET_FIFO(T1856_i0, 1);
	GET_FIFO(T1856_i1, 3);
	Butterfly(T1856_i0, T1856_i1, &T1856_o0, &T1856_o1, T1856_W);
	PUT_FIFO(T1856_o0, 0);
	PUT_FIFO(T1856_o1, 1);

	GET_FIFO(T1857_i0, 1);
	GET_FIFO(T1857_i1, 3);
	Butterfly(T1857_i0, T1857_i1, &T1857_o0, &T1857_o1, T1857_W);
	PUT_FIFO(T1857_o0, 0);
	PUT_FIFO(T1857_o1, 1);

	GET_FIFO(T1858_i0, 1);
	GET_FIFO(T1858_i1, 3);
	Butterfly(T1858_i0, T1858_i1, &T1858_o0, &T1858_o1, T1858_W);
	PUT_FIFO(T1858_o0, 0);
	PUT_FIFO(T1858_o1, 1);

	GET_FIFO(T1859_i0, 1);
	GET_FIFO(T1859_i1, 3);
	Butterfly(T1859_i0, T1859_i1, &T1859_o0, &T1859_o1, T1859_W);
	PUT_FIFO(T1859_o0, 0);
	PUT_FIFO(T1859_o1, 1);

	GET_FIFO(T1860_i0, 1);
	GET_FIFO(T1860_i1, 3);
	Butterfly(T1860_i0, T1860_i1, &T1860_o0, &T1860_o1, T1860_W);
	PUT_FIFO(T1860_o0, 0);
	PUT_FIFO(T1860_o1, 1);

	GET_FIFO(T1861_i0, 1);
	GET_FIFO(T1861_i1, 3);
	Butterfly(T1861_i0, T1861_i1, &T1861_o0, &T1861_o1, T1861_W);
	PUT_FIFO(T1861_o0, 0);
	PUT_FIFO(T1861_o1, 1);

	GET_FIFO(T1862_i0, 1);
	GET_FIFO(T1862_i1, 3);
	Butterfly(T1862_i0, T1862_i1, &T1862_o0, &T1862_o1, T1862_W);
	PUT_FIFO(T1862_o0, 0);
	PUT_FIFO(T1862_o1, 1);

	GET_FIFO(T1863_i0, 1);
	GET_FIFO(T1863_i1, 3);
	Butterfly(T1863_i0, T1863_i1, &T1863_o0, &T1863_o1, T1863_W);
	PUT_FIFO(T1863_o0, 0);
	PUT_FIFO(T1863_o1, 1);

	GET_FIFO(T1864_i0, 1);
	GET_FIFO(T1864_i1, 3);
	Butterfly(T1864_i0, T1864_i1, &T1864_o0, &T1864_o1, T1864_W);
	PUT_FIFO(T1864_o0, 0);
	PUT_FIFO(T1864_o1, 1);

	GET_FIFO(T1865_i0, 1);
	GET_FIFO(T1865_i1, 3);
	Butterfly(T1865_i0, T1865_i1, &T1865_o0, &T1865_o1, T1865_W);
	PUT_FIFO(T1865_o0, 0);
	PUT_FIFO(T1865_o1, 1);

	GET_FIFO(T1866_i0, 1);
	GET_FIFO(T1866_i1, 3);
	Butterfly(T1866_i0, T1866_i1, &T1866_o0, &T1866_o1, T1866_W);
	PUT_FIFO(T1866_o0, 0);
	PUT_FIFO(T1866_o1, 1);

	GET_FIFO(T1867_i0, 1);
	GET_FIFO(T1867_i1, 3);
	Butterfly(T1867_i0, T1867_i1, &T1867_o0, &T1867_o1, T1867_W);
	PUT_FIFO(T1867_o0, 0);
	PUT_FIFO(T1867_o1, 1);

	GET_FIFO(T1868_i0, 1);
	GET_FIFO(T1868_i1, 3);
	Butterfly(T1868_i0, T1868_i1, &T1868_o0, &T1868_o1, T1868_W);
	PUT_FIFO(T1868_o0, 0);
	PUT_FIFO(T1868_o1, 1);

	GET_FIFO(T1869_i0, 1);
	GET_FIFO(T1869_i1, 3);
	Butterfly(T1869_i0, T1869_i1, &T1869_o0, &T1869_o1, T1869_W);
	PUT_FIFO(T1869_o0, 0);
	PUT_FIFO(T1869_o1, 1);

	GET_FIFO(T1870_i0, 1);
	GET_FIFO(T1870_i1, 3);
	Butterfly(T1870_i0, T1870_i1, &T1870_o0, &T1870_o1, T1870_W);
	PUT_FIFO(T1870_o0, 0);
	PUT_FIFO(T1870_o1, 1);

	GET_FIFO(T1871_i0, 1);
	GET_FIFO(T1871_i1, 3);
	Butterfly(T1871_i0, T1871_i1, &T1871_o0, &T1871_o1, T1871_W);
	PUT_FIFO(T1871_o0, 0);
	PUT_FIFO(T1871_o1, 1);

	GET_FIFO(T1872_i0, 1);
	GET_FIFO(T1872_i1, 3);
	Butterfly(T1872_i0, T1872_i1, &T1872_o0, &T1872_o1, T1872_W);
	PUT_FIFO(T1872_o0, 0);
	PUT_FIFO(T1872_o1, 1);

	GET_FIFO(T1873_i0, 1);
	GET_FIFO(T1873_i1, 3);
	Butterfly(T1873_i0, T1873_i1, &T1873_o0, &T1873_o1, T1873_W);
	PUT_FIFO(T1873_o0, 0);
	PUT_FIFO(T1873_o1, 1);

	GET_FIFO(T1874_i0, 1);
	GET_FIFO(T1874_i1, 3);
	Butterfly(T1874_i0, T1874_i1, &T1874_o0, &T1874_o1, T1874_W);
	PUT_FIFO(T1874_o0, 0);
	PUT_FIFO(T1874_o1, 1);

	GET_FIFO(T1875_i0, 1);
	GET_FIFO(T1875_i1, 3);
	Butterfly(T1875_i0, T1875_i1, &T1875_o0, &T1875_o1, T1875_W);
	PUT_FIFO(T1875_o0, 0);
	PUT_FIFO(T1875_o1, 1);

	GET_FIFO(T1876_i0, 1);
	GET_FIFO(T1876_i1, 3);
	Butterfly(T1876_i0, T1876_i1, &T1876_o0, &T1876_o1, T1876_W);
	PUT_FIFO(T1876_o0, 0);
	PUT_FIFO(T1876_o1, 1);

	GET_FIFO(T1877_i0, 1);
	GET_FIFO(T1877_i1, 3);
	Butterfly(T1877_i0, T1877_i1, &T1877_o0, &T1877_o1, T1877_W);
	PUT_FIFO(T1877_o0, 0);
	PUT_FIFO(T1877_o1, 1);

	GET_FIFO(T1878_i0, 1);
	GET_FIFO(T1878_i1, 3);
	Butterfly(T1878_i0, T1878_i1, &T1878_o0, &T1878_o1, T1878_W);
	PUT_FIFO(T1878_o0, 0);
	PUT_FIFO(T1878_o1, 1);

	GET_FIFO(T1879_i0, 1);
	GET_FIFO(T1879_i1, 3);
	Butterfly(T1879_i0, T1879_i1, &T1879_o0, &T1879_o1, T1879_W);
	PUT_FIFO(T1879_o0, 0);
	PUT_FIFO(T1879_o1, 1);

	GET_FIFO(T1880_i0, 1);
	GET_FIFO(T1880_i1, 3);
	Butterfly(T1880_i0, T1880_i1, &T1880_o0, &T1880_o1, T1880_W);
	PUT_FIFO(T1880_o0, 0);
	PUT_FIFO(T1880_o1, 1);

	GET_FIFO(T1881_i0, 1);
	GET_FIFO(T1881_i1, 3);
	Butterfly(T1881_i0, T1881_i1, &T1881_o0, &T1881_o1, T1881_W);
	PUT_FIFO(T1881_o0, 0);
	PUT_FIFO(T1881_o1, 1);

	GET_FIFO(T1882_i0, 1);
	GET_FIFO(T1882_i1, 3);
	Butterfly(T1882_i0, T1882_i1, &T1882_o0, &T1882_o1, T1882_W);
	PUT_FIFO(T1882_o0, 0);
	PUT_FIFO(T1882_o1, 1);

	GET_FIFO(T1883_i0, 1);
	GET_FIFO(T1883_i1, 3);
	Butterfly(T1883_i0, T1883_i1, &T1883_o0, &T1883_o1, T1883_W);
	PUT_FIFO(T1883_o0, 0);
	PUT_FIFO(T1883_o1, 1);

	GET_FIFO(T1884_i0, 1);
	GET_FIFO(T1884_i1, 3);
	Butterfly(T1884_i0, T1884_i1, &T1884_o0, &T1884_o1, T1884_W);
	PUT_FIFO(T1884_o0, 0);
	PUT_FIFO(T1884_o1, 1);

	GET_FIFO(T1885_i0, 1);
	GET_FIFO(T1885_i1, 3);
	Butterfly(T1885_i0, T1885_i1, &T1885_o0, &T1885_o1, T1885_W);
	PUT_FIFO(T1885_o0, 0);
	PUT_FIFO(T1885_o1, 1);

	GET_FIFO(T1886_i0, 1);
	GET_FIFO(T1886_i1, 3);
	Butterfly(T1886_i0, T1886_i1, &T1886_o0, &T1886_o1, T1886_W);
	PUT_FIFO(T1886_o0, 0);
	PUT_FIFO(T1886_o1, 1);

	GET_FIFO(T1887_i0, 1);
	GET_FIFO(T1887_i1, 3);
	Butterfly(T1887_i0, T1887_i1, &T1887_o0, &T1887_o1, T1887_W);
	PUT_FIFO(T1887_o0, 0);
	PUT_FIFO(T1887_o1, 1);

	GET_FIFO(T1888_i0, 1);
	GET_FIFO(T1888_i1, 3);
	Butterfly(T1888_i0, T1888_i1, &T1888_o0, &T1888_o1, T1888_W);
	PUT_FIFO(T1888_o0, 0);
	PUT_FIFO(T1888_o1, 1);

	GET_FIFO(T1889_i0, 1);
	GET_FIFO(T1889_i1, 3);
	Butterfly(T1889_i0, T1889_i1, &T1889_o0, &T1889_o1, T1889_W);
	PUT_FIFO(T1889_o0, 0);
	PUT_FIFO(T1889_o1, 1);

	GET_FIFO(T1890_i0, 1);
	GET_FIFO(T1890_i1, 3);
	Butterfly(T1890_i0, T1890_i1, &T1890_o0, &T1890_o1, T1890_W);
	PUT_FIFO(T1890_o0, 0);
	PUT_FIFO(T1890_o1, 1);

	GET_FIFO(T1891_i0, 1);
	GET_FIFO(T1891_i1, 3);
	Butterfly(T1891_i0, T1891_i1, &T1891_o0, &T1891_o1, T1891_W);
	PUT_FIFO(T1891_o0, 0);
	PUT_FIFO(T1891_o1, 1);

	GET_FIFO(T1892_i0, 1);
	GET_FIFO(T1892_i1, 3);
	Butterfly(T1892_i0, T1892_i1, &T1892_o0, &T1892_o1, T1892_W);
	PUT_FIFO(T1892_o0, 0);
	PUT_FIFO(T1892_o1, 1);

	GET_FIFO(T1893_i0, 1);
	GET_FIFO(T1893_i1, 3);
	Butterfly(T1893_i0, T1893_i1, &T1893_o0, &T1893_o1, T1893_W);
	PUT_FIFO(T1893_o0, 0);
	PUT_FIFO(T1893_o1, 1);

	GET_FIFO(T1894_i0, 1);
	GET_FIFO(T1894_i1, 3);
	Butterfly(T1894_i0, T1894_i1, &T1894_o0, &T1894_o1, T1894_W);
	PUT_FIFO(T1894_o0, 0);
	PUT_FIFO(T1894_o1, 1);

	GET_FIFO(T1895_i0, 1);
	GET_FIFO(T1895_i1, 3);
	Butterfly(T1895_i0, T1895_i1, &T1895_o0, &T1895_o1, T1895_W);
	PUT_FIFO(T1895_o0, 0);
	PUT_FIFO(T1895_o1, 1);

	GET_FIFO(T1896_i0, 1);
	GET_FIFO(T1896_i1, 3);
	Butterfly(T1896_i0, T1896_i1, &T1896_o0, &T1896_o1, T1896_W);
	PUT_FIFO(T1896_o0, 0);
	PUT_FIFO(T1896_o1, 1);

	GET_FIFO(T1897_i0, 1);
	GET_FIFO(T1897_i1, 3);
	Butterfly(T1897_i0, T1897_i1, &T1897_o0, &T1897_o1, T1897_W);
	PUT_FIFO(T1897_o0, 0);
	PUT_FIFO(T1897_o1, 1);

	GET_FIFO(T1898_i0, 1);
	GET_FIFO(T1898_i1, 3);
	Butterfly(T1898_i0, T1898_i1, &T1898_o0, &T1898_o1, T1898_W);
	PUT_FIFO(T1898_o0, 0);
	PUT_FIFO(T1898_o1, 1);

	GET_FIFO(T1899_i0, 1);
	GET_FIFO(T1899_i1, 3);
	Butterfly(T1899_i0, T1899_i1, &T1899_o0, &T1899_o1, T1899_W);
	PUT_FIFO(T1899_o0, 0);
	PUT_FIFO(T1899_o1, 1);

	GET_FIFO(T1900_i0, 1);
	GET_FIFO(T1900_i1, 3);
	Butterfly(T1900_i0, T1900_i1, &T1900_o0, &T1900_o1, T1900_W);
	PUT_FIFO(T1900_o0, 0);
	PUT_FIFO(T1900_o1, 1);

	GET_FIFO(T1901_i0, 1);
	GET_FIFO(T1901_i1, 3);
	Butterfly(T1901_i0, T1901_i1, &T1901_o0, &T1901_o1, T1901_W);
	PUT_FIFO(T1901_o0, 0);
	PUT_FIFO(T1901_o1, 1);

	GET_FIFO(T1902_i0, 1);
	GET_FIFO(T1902_i1, 3);
	Butterfly(T1902_i0, T1902_i1, &T1902_o0, &T1902_o1, T1902_W);
	PUT_FIFO(T1902_o0, 0);
	PUT_FIFO(T1902_o1, 1);

	GET_FIFO(T1903_i0, 1);
	GET_FIFO(T1903_i1, 3);
	Butterfly(T1903_i0, T1903_i1, &T1903_o0, &T1903_o1, T1903_W);
	PUT_FIFO(T1903_o0, 0);
	PUT_FIFO(T1903_o1, 1);

	GET_FIFO(T1904_i0, 1);
	GET_FIFO(T1904_i1, 3);
	Butterfly(T1904_i0, T1904_i1, &T1904_o0, &T1904_o1, T1904_W);
	PUT_FIFO(T1904_o0, 0);
	PUT_FIFO(T1904_o1, 1);

	GET_FIFO(T1905_i0, 1);
	GET_FIFO(T1905_i1, 3);
	Butterfly(T1905_i0, T1905_i1, &T1905_o0, &T1905_o1, T1905_W);
	PUT_FIFO(T1905_o0, 0);
	PUT_FIFO(T1905_o1, 1);

	GET_FIFO(T1906_i0, 1);
	GET_FIFO(T1906_i1, 3);
	Butterfly(T1906_i0, T1906_i1, &T1906_o0, &T1906_o1, T1906_W);
	PUT_FIFO(T1906_o0, 0);
	PUT_FIFO(T1906_o1, 1);

	GET_FIFO(T1907_i0, 1);
	GET_FIFO(T1907_i1, 3);
	Butterfly(T1907_i0, T1907_i1, &T1907_o0, &T1907_o1, T1907_W);
	PUT_FIFO(T1907_o0, 0);
	PUT_FIFO(T1907_o1, 1);

	GET_FIFO(T1908_i0, 1);
	GET_FIFO(T1908_i1, 3);
	Butterfly(T1908_i0, T1908_i1, &T1908_o0, &T1908_o1, T1908_W);
	PUT_FIFO(T1908_o0, 0);
	PUT_FIFO(T1908_o1, 1);

	GET_FIFO(T1909_i0, 1);
	GET_FIFO(T1909_i1, 3);
	Butterfly(T1909_i0, T1909_i1, &T1909_o0, &T1909_o1, T1909_W);
	PUT_FIFO(T1909_o0, 0);
	PUT_FIFO(T1909_o1, 1);

	GET_FIFO(T1910_i0, 1);
	GET_FIFO(T1910_i1, 3);
	Butterfly(T1910_i0, T1910_i1, &T1910_o0, &T1910_o1, T1910_W);
	PUT_FIFO(T1910_o0, 0);
	PUT_FIFO(T1910_o1, 1);

	GET_FIFO(T1911_i0, 1);
	GET_FIFO(T1911_i1, 3);
	Butterfly(T1911_i0, T1911_i1, &T1911_o0, &T1911_o1, T1911_W);
	PUT_FIFO(T1911_o0, 0);
	PUT_FIFO(T1911_o1, 1);

	GET_FIFO(T1912_i0, 1);
	GET_FIFO(T1912_i1, 3);
	Butterfly(T1912_i0, T1912_i1, &T1912_o0, &T1912_o1, T1912_W);
	PUT_FIFO(T1912_o0, 0);
	PUT_FIFO(T1912_o1, 1);

	GET_FIFO(T1913_i0, 1);
	GET_FIFO(T1913_i1, 3);
	Butterfly(T1913_i0, T1913_i1, &T1913_o0, &T1913_o1, T1913_W);
	PUT_FIFO(T1913_o0, 0);
	PUT_FIFO(T1913_o1, 1);

	GET_FIFO(T1914_i0, 1);
	GET_FIFO(T1914_i1, 3);
	Butterfly(T1914_i0, T1914_i1, &T1914_o0, &T1914_o1, T1914_W);
	PUT_FIFO(T1914_o0, 0);
	PUT_FIFO(T1914_o1, 1);

	GET_FIFO(T1915_i0, 1);
	GET_FIFO(T1915_i1, 3);
	Butterfly(T1915_i0, T1915_i1, &T1915_o0, &T1915_o1, T1915_W);
	PUT_FIFO(T1915_o0, 0);
	PUT_FIFO(T1915_o1, 1);

	GET_FIFO(T1916_i0, 1);
	GET_FIFO(T1916_i1, 3);
	Butterfly(T1916_i0, T1916_i1, &T1916_o0, &T1916_o1, T1916_W);
	PUT_FIFO(T1916_o0, 0);
	PUT_FIFO(T1916_o1, 1);

	GET_FIFO(T1917_i0, 1);
	GET_FIFO(T1917_i1, 3);
	Butterfly(T1917_i0, T1917_i1, &T1917_o0, &T1917_o1, T1917_W);
	PUT_FIFO(T1917_o0, 0);
	PUT_FIFO(T1917_o1, 1);

	GET_FIFO(T1918_i0, 1);
	GET_FIFO(T1918_i1, 3);
	Butterfly(T1918_i0, T1918_i1, &T1918_o0, &T1918_o1, T1918_W);
	PUT_FIFO(T1918_o0, 0);
	PUT_FIFO(T1918_o1, 1);

	GET_FIFO(T1919_i0, 1);
	GET_FIFO(T1919_i1, 3);
	Butterfly(T1919_i0, T1919_i1, &T1919_o0, &T1919_o1, T1919_W);
	PUT_FIFO(T1919_o0, 0);
	PUT_FIFO(T1919_o1, 1);

	GET_FIFO(T1920_i0, 0);
	GET_FIFO(T1920_i1, 2);
	Butterfly(T1920_i0, T1920_i1, &T1920_o0, &T1920_o1, T1920_W);
	PUT_FIFO(T1920_o0, 2);
	PUT_FIFO(T1920_o1, 3);

	GET_FIFO(T1921_i0, 0);
	GET_FIFO(T1921_i1, 2);
	Butterfly(T1921_i0, T1921_i1, &T1921_o0, &T1921_o1, T1921_W);
	PUT_FIFO(T1921_o0, 2);
	PUT_FIFO(T1921_o1, 3);

	GET_FIFO(T1922_i0, 0);
	GET_FIFO(T1922_i1, 2);
	Butterfly(T1922_i0, T1922_i1, &T1922_o0, &T1922_o1, T1922_W);
	PUT_FIFO(T1922_o0, 2);
	PUT_FIFO(T1922_o1, 3);

	GET_FIFO(T1923_i0, 0);
	GET_FIFO(T1923_i1, 2);
	Butterfly(T1923_i0, T1923_i1, &T1923_o0, &T1923_o1, T1923_W);
	PUT_FIFO(T1923_o0, 2);
	PUT_FIFO(T1923_o1, 3);

	GET_FIFO(T1924_i0, 0);
	GET_FIFO(T1924_i1, 2);
	Butterfly(T1924_i0, T1924_i1, &T1924_o0, &T1924_o1, T1924_W);
	PUT_FIFO(T1924_o0, 2);
	PUT_FIFO(T1924_o1, 3);

	GET_FIFO(T1925_i0, 0);
	GET_FIFO(T1925_i1, 2);
	Butterfly(T1925_i0, T1925_i1, &T1925_o0, &T1925_o1, T1925_W);
	PUT_FIFO(T1925_o0, 2);
	PUT_FIFO(T1925_o1, 3);

	GET_FIFO(T1926_i0, 0);
	GET_FIFO(T1926_i1, 2);
	Butterfly(T1926_i0, T1926_i1, &T1926_o0, &T1926_o1, T1926_W);
	PUT_FIFO(T1926_o0, 2);
	PUT_FIFO(T1926_o1, 3);

	GET_FIFO(T1927_i0, 0);
	GET_FIFO(T1927_i1, 2);
	Butterfly(T1927_i0, T1927_i1, &T1927_o0, &T1927_o1, T1927_W);
	PUT_FIFO(T1927_o0, 2);
	PUT_FIFO(T1927_o1, 3);

	GET_FIFO(T1928_i0, 0);
	GET_FIFO(T1928_i1, 2);
	Butterfly(T1928_i0, T1928_i1, &T1928_o0, &T1928_o1, T1928_W);
	PUT_FIFO(T1928_o0, 2);
	PUT_FIFO(T1928_o1, 3);

	GET_FIFO(T1929_i0, 0);
	GET_FIFO(T1929_i1, 2);
	Butterfly(T1929_i0, T1929_i1, &T1929_o0, &T1929_o1, T1929_W);
	PUT_FIFO(T1929_o0, 2);
	PUT_FIFO(T1929_o1, 3);

	GET_FIFO(T1930_i0, 0);
	GET_FIFO(T1930_i1, 2);
	Butterfly(T1930_i0, T1930_i1, &T1930_o0, &T1930_o1, T1930_W);
	PUT_FIFO(T1930_o0, 2);
	PUT_FIFO(T1930_o1, 3);

	GET_FIFO(T1931_i0, 0);
	GET_FIFO(T1931_i1, 2);
	Butterfly(T1931_i0, T1931_i1, &T1931_o0, &T1931_o1, T1931_W);
	PUT_FIFO(T1931_o0, 2);
	PUT_FIFO(T1931_o1, 3);

	GET_FIFO(T1932_i0, 0);
	GET_FIFO(T1932_i1, 2);
	Butterfly(T1932_i0, T1932_i1, &T1932_o0, &T1932_o1, T1932_W);
	PUT_FIFO(T1932_o0, 2);
	PUT_FIFO(T1932_o1, 3);

	GET_FIFO(T1933_i0, 0);
	GET_FIFO(T1933_i1, 2);
	Butterfly(T1933_i0, T1933_i1, &T1933_o0, &T1933_o1, T1933_W);
	PUT_FIFO(T1933_o0, 2);
	PUT_FIFO(T1933_o1, 3);

	GET_FIFO(T1934_i0, 0);
	GET_FIFO(T1934_i1, 2);
	Butterfly(T1934_i0, T1934_i1, &T1934_o0, &T1934_o1, T1934_W);
	PUT_FIFO(T1934_o0, 2);
	PUT_FIFO(T1934_o1, 3);

	GET_FIFO(T1935_i0, 0);
	GET_FIFO(T1935_i1, 2);
	Butterfly(T1935_i0, T1935_i1, &T1935_o0, &T1935_o1, T1935_W);
	PUT_FIFO(T1935_o0, 2);
	PUT_FIFO(T1935_o1, 3);

	GET_FIFO(T1936_i0, 0);
	GET_FIFO(T1936_i1, 2);
	Butterfly(T1936_i0, T1936_i1, &T1936_o0, &T1936_o1, T1936_W);
	PUT_FIFO(T1936_o0, 2);
	PUT_FIFO(T1936_o1, 3);

	GET_FIFO(T1937_i0, 0);
	GET_FIFO(T1937_i1, 2);
	Butterfly(T1937_i0, T1937_i1, &T1937_o0, &T1937_o1, T1937_W);
	PUT_FIFO(T1937_o0, 2);
	PUT_FIFO(T1937_o1, 3);

	GET_FIFO(T1938_i0, 0);
	GET_FIFO(T1938_i1, 2);
	Butterfly(T1938_i0, T1938_i1, &T1938_o0, &T1938_o1, T1938_W);
	PUT_FIFO(T1938_o0, 2);
	PUT_FIFO(T1938_o1, 3);

	GET_FIFO(T1939_i0, 0);
	GET_FIFO(T1939_i1, 2);
	Butterfly(T1939_i0, T1939_i1, &T1939_o0, &T1939_o1, T1939_W);
	PUT_FIFO(T1939_o0, 2);
	PUT_FIFO(T1939_o1, 3);

	GET_FIFO(T1940_i0, 0);
	GET_FIFO(T1940_i1, 2);
	Butterfly(T1940_i0, T1940_i1, &T1940_o0, &T1940_o1, T1940_W);
	PUT_FIFO(T1940_o0, 2);
	PUT_FIFO(T1940_o1, 3);

	GET_FIFO(T1941_i0, 0);
	GET_FIFO(T1941_i1, 2);
	Butterfly(T1941_i0, T1941_i1, &T1941_o0, &T1941_o1, T1941_W);
	PUT_FIFO(T1941_o0, 2);
	PUT_FIFO(T1941_o1, 3);

	GET_FIFO(T1942_i0, 0);
	GET_FIFO(T1942_i1, 2);
	Butterfly(T1942_i0, T1942_i1, &T1942_o0, &T1942_o1, T1942_W);
	PUT_FIFO(T1942_o0, 2);
	PUT_FIFO(T1942_o1, 3);

	GET_FIFO(T1943_i0, 0);
	GET_FIFO(T1943_i1, 2);
	Butterfly(T1943_i0, T1943_i1, &T1943_o0, &T1943_o1, T1943_W);
	PUT_FIFO(T1943_o0, 2);
	PUT_FIFO(T1943_o1, 3);

	GET_FIFO(T1944_i0, 0);
	GET_FIFO(T1944_i1, 2);
	Butterfly(T1944_i0, T1944_i1, &T1944_o0, &T1944_o1, T1944_W);
	PUT_FIFO(T1944_o0, 2);
	PUT_FIFO(T1944_o1, 3);

	GET_FIFO(T1945_i0, 0);
	GET_FIFO(T1945_i1, 2);
	Butterfly(T1945_i0, T1945_i1, &T1945_o0, &T1945_o1, T1945_W);
	PUT_FIFO(T1945_o0, 2);
	PUT_FIFO(T1945_o1, 3);

	GET_FIFO(T1946_i0, 0);
	GET_FIFO(T1946_i1, 2);
	Butterfly(T1946_i0, T1946_i1, &T1946_o0, &T1946_o1, T1946_W);
	PUT_FIFO(T1946_o0, 2);
	PUT_FIFO(T1946_o1, 3);

	GET_FIFO(T1947_i0, 0);
	GET_FIFO(T1947_i1, 2);
	Butterfly(T1947_i0, T1947_i1, &T1947_o0, &T1947_o1, T1947_W);
	PUT_FIFO(T1947_o0, 2);
	PUT_FIFO(T1947_o1, 3);

	GET_FIFO(T1948_i0, 0);
	GET_FIFO(T1948_i1, 2);
	Butterfly(T1948_i0, T1948_i1, &T1948_o0, &T1948_o1, T1948_W);
	PUT_FIFO(T1948_o0, 2);
	PUT_FIFO(T1948_o1, 3);

	GET_FIFO(T1949_i0, 0);
	GET_FIFO(T1949_i1, 2);
	Butterfly(T1949_i0, T1949_i1, &T1949_o0, &T1949_o1, T1949_W);
	PUT_FIFO(T1949_o0, 2);
	PUT_FIFO(T1949_o1, 3);

	GET_FIFO(T1950_i0, 0);
	GET_FIFO(T1950_i1, 2);
	Butterfly(T1950_i0, T1950_i1, &T1950_o0, &T1950_o1, T1950_W);
	PUT_FIFO(T1950_o0, 2);
	PUT_FIFO(T1950_o1, 3);

	GET_FIFO(T1951_i0, 0);
	GET_FIFO(T1951_i1, 2);
	Butterfly(T1951_i0, T1951_i1, &T1951_o0, &T1951_o1, T1951_W);
	PUT_FIFO(T1951_o0, 2);
	PUT_FIFO(T1951_o1, 3);

	GET_FIFO(T1952_i0, 0);
	GET_FIFO(T1952_i1, 2);
	Butterfly(T1952_i0, T1952_i1, &T1952_o0, &T1952_o1, T1952_W);
	PUT_FIFO(T1952_o0, 2);
	PUT_FIFO(T1952_o1, 3);

	GET_FIFO(T1953_i0, 0);
	GET_FIFO(T1953_i1, 2);
	Butterfly(T1953_i0, T1953_i1, &T1953_o0, &T1953_o1, T1953_W);
	PUT_FIFO(T1953_o0, 2);
	PUT_FIFO(T1953_o1, 3);

	GET_FIFO(T1954_i0, 0);
	GET_FIFO(T1954_i1, 2);
	Butterfly(T1954_i0, T1954_i1, &T1954_o0, &T1954_o1, T1954_W);
	PUT_FIFO(T1954_o0, 2);
	PUT_FIFO(T1954_o1, 3);

	GET_FIFO(T1955_i0, 0);
	GET_FIFO(T1955_i1, 2);
	Butterfly(T1955_i0, T1955_i1, &T1955_o0, &T1955_o1, T1955_W);
	PUT_FIFO(T1955_o0, 2);
	PUT_FIFO(T1955_o1, 3);

	GET_FIFO(T1956_i0, 0);
	GET_FIFO(T1956_i1, 2);
	Butterfly(T1956_i0, T1956_i1, &T1956_o0, &T1956_o1, T1956_W);
	PUT_FIFO(T1956_o0, 2);
	PUT_FIFO(T1956_o1, 3);

	GET_FIFO(T1957_i0, 0);
	GET_FIFO(T1957_i1, 2);
	Butterfly(T1957_i0, T1957_i1, &T1957_o0, &T1957_o1, T1957_W);
	PUT_FIFO(T1957_o0, 2);
	PUT_FIFO(T1957_o1, 3);

	GET_FIFO(T1958_i0, 0);
	GET_FIFO(T1958_i1, 2);
	Butterfly(T1958_i0, T1958_i1, &T1958_o0, &T1958_o1, T1958_W);
	PUT_FIFO(T1958_o0, 2);
	PUT_FIFO(T1958_o1, 3);

	GET_FIFO(T1959_i0, 0);
	GET_FIFO(T1959_i1, 2);
	Butterfly(T1959_i0, T1959_i1, &T1959_o0, &T1959_o1, T1959_W);
	PUT_FIFO(T1959_o0, 2);
	PUT_FIFO(T1959_o1, 3);

	GET_FIFO(T1960_i0, 0);
	GET_FIFO(T1960_i1, 2);
	Butterfly(T1960_i0, T1960_i1, &T1960_o0, &T1960_o1, T1960_W);
	PUT_FIFO(T1960_o0, 2);
	PUT_FIFO(T1960_o1, 3);

	GET_FIFO(T1961_i0, 0);
	GET_FIFO(T1961_i1, 2);
	Butterfly(T1961_i0, T1961_i1, &T1961_o0, &T1961_o1, T1961_W);
	PUT_FIFO(T1961_o0, 2);
	PUT_FIFO(T1961_o1, 3);

	GET_FIFO(T1962_i0, 0);
	GET_FIFO(T1962_i1, 2);
	Butterfly(T1962_i0, T1962_i1, &T1962_o0, &T1962_o1, T1962_W);
	PUT_FIFO(T1962_o0, 2);
	PUT_FIFO(T1962_o1, 3);

	GET_FIFO(T1963_i0, 0);
	GET_FIFO(T1963_i1, 2);
	Butterfly(T1963_i0, T1963_i1, &T1963_o0, &T1963_o1, T1963_W);
	PUT_FIFO(T1963_o0, 2);
	PUT_FIFO(T1963_o1, 3);

	GET_FIFO(T1964_i0, 0);
	GET_FIFO(T1964_i1, 2);
	Butterfly(T1964_i0, T1964_i1, &T1964_o0, &T1964_o1, T1964_W);
	PUT_FIFO(T1964_o0, 2);
	PUT_FIFO(T1964_o1, 3);

	GET_FIFO(T1965_i0, 0);
	GET_FIFO(T1965_i1, 2);
	Butterfly(T1965_i0, T1965_i1, &T1965_o0, &T1965_o1, T1965_W);
	PUT_FIFO(T1965_o0, 2);
	PUT_FIFO(T1965_o1, 3);

	GET_FIFO(T1966_i0, 0);
	GET_FIFO(T1966_i1, 2);
	Butterfly(T1966_i0, T1966_i1, &T1966_o0, &T1966_o1, T1966_W);
	PUT_FIFO(T1966_o0, 2);
	PUT_FIFO(T1966_o1, 3);

	GET_FIFO(T1967_i0, 0);
	GET_FIFO(T1967_i1, 2);
	Butterfly(T1967_i0, T1967_i1, &T1967_o0, &T1967_o1, T1967_W);
	PUT_FIFO(T1967_o0, 2);
	PUT_FIFO(T1967_o1, 3);

	GET_FIFO(T1968_i0, 0);
	GET_FIFO(T1968_i1, 2);
	Butterfly(T1968_i0, T1968_i1, &T1968_o0, &T1968_o1, T1968_W);
	PUT_FIFO(T1968_o0, 2);
	PUT_FIFO(T1968_o1, 3);

	GET_FIFO(T1969_i0, 0);
	GET_FIFO(T1969_i1, 2);
	Butterfly(T1969_i0, T1969_i1, &T1969_o0, &T1969_o1, T1969_W);
	PUT_FIFO(T1969_o0, 2);
	PUT_FIFO(T1969_o1, 3);

	GET_FIFO(T1970_i0, 0);
	GET_FIFO(T1970_i1, 2);
	Butterfly(T1970_i0, T1970_i1, &T1970_o0, &T1970_o1, T1970_W);
	PUT_FIFO(T1970_o0, 2);
	PUT_FIFO(T1970_o1, 3);

	GET_FIFO(T1971_i0, 0);
	GET_FIFO(T1971_i1, 2);
	Butterfly(T1971_i0, T1971_i1, &T1971_o0, &T1971_o1, T1971_W);
	PUT_FIFO(T1971_o0, 2);
	PUT_FIFO(T1971_o1, 3);

	GET_FIFO(T1972_i0, 0);
	GET_FIFO(T1972_i1, 2);
	Butterfly(T1972_i0, T1972_i1, &T1972_o0, &T1972_o1, T1972_W);
	PUT_FIFO(T1972_o0, 2);
	PUT_FIFO(T1972_o1, 3);

	GET_FIFO(T1973_i0, 0);
	GET_FIFO(T1973_i1, 2);
	Butterfly(T1973_i0, T1973_i1, &T1973_o0, &T1973_o1, T1973_W);
	PUT_FIFO(T1973_o0, 2);
	PUT_FIFO(T1973_o1, 3);

	GET_FIFO(T1974_i0, 0);
	GET_FIFO(T1974_i1, 2);
	Butterfly(T1974_i0, T1974_i1, &T1974_o0, &T1974_o1, T1974_W);
	PUT_FIFO(T1974_o0, 2);
	PUT_FIFO(T1974_o1, 3);

	GET_FIFO(T1975_i0, 0);
	GET_FIFO(T1975_i1, 2);
	Butterfly(T1975_i0, T1975_i1, &T1975_o0, &T1975_o1, T1975_W);
	PUT_FIFO(T1975_o0, 2);
	PUT_FIFO(T1975_o1, 3);

	GET_FIFO(T1976_i0, 0);
	GET_FIFO(T1976_i1, 2);
	Butterfly(T1976_i0, T1976_i1, &T1976_o0, &T1976_o1, T1976_W);
	PUT_FIFO(T1976_o0, 2);
	PUT_FIFO(T1976_o1, 3);

	GET_FIFO(T1977_i0, 0);
	GET_FIFO(T1977_i1, 2);
	Butterfly(T1977_i0, T1977_i1, &T1977_o0, &T1977_o1, T1977_W);
	PUT_FIFO(T1977_o0, 2);
	PUT_FIFO(T1977_o1, 3);

	GET_FIFO(T1978_i0, 0);
	GET_FIFO(T1978_i1, 2);
	Butterfly(T1978_i0, T1978_i1, &T1978_o0, &T1978_o1, T1978_W);
	PUT_FIFO(T1978_o0, 2);
	PUT_FIFO(T1978_o1, 3);

	GET_FIFO(T1979_i0, 0);
	GET_FIFO(T1979_i1, 2);
	Butterfly(T1979_i0, T1979_i1, &T1979_o0, &T1979_o1, T1979_W);
	PUT_FIFO(T1979_o0, 2);
	PUT_FIFO(T1979_o1, 3);

	GET_FIFO(T1980_i0, 0);
	GET_FIFO(T1980_i1, 2);
	Butterfly(T1980_i0, T1980_i1, &T1980_o0, &T1980_o1, T1980_W);
	PUT_FIFO(T1980_o0, 2);
	PUT_FIFO(T1980_o1, 3);

	GET_FIFO(T1981_i0, 0);
	GET_FIFO(T1981_i1, 2);
	Butterfly(T1981_i0, T1981_i1, &T1981_o0, &T1981_o1, T1981_W);
	PUT_FIFO(T1981_o0, 2);
	PUT_FIFO(T1981_o1, 3);

	GET_FIFO(T1982_i0, 0);
	GET_FIFO(T1982_i1, 2);
	Butterfly(T1982_i0, T1982_i1, &T1982_o0, &T1982_o1, T1982_W);
	PUT_FIFO(T1982_o0, 2);
	PUT_FIFO(T1982_o1, 3);

	GET_FIFO(T1983_i0, 0);
	GET_FIFO(T1983_i1, 2);
	Butterfly(T1983_i0, T1983_i1, &T1983_o0, &T1983_o1, T1983_W);
	PUT_FIFO(T1983_o0, 2);
	PUT_FIFO(T1983_o1, 3);

	GET_FIFO(T1984_i0, 1);
	GET_FIFO(T1984_i1, 3);
	Butterfly(T1984_i0, T1984_i1, &T1984_o0, &T1984_o1, T1984_W);
	PUT_FIFO(T1984_o0, 2);
	PUT_FIFO(T1984_o1, 3);

	GET_FIFO(T1985_i0, 1);
	GET_FIFO(T1985_i1, 3);
	Butterfly(T1985_i0, T1985_i1, &T1985_o0, &T1985_o1, T1985_W);
	PUT_FIFO(T1985_o0, 2);
	PUT_FIFO(T1985_o1, 3);

	GET_FIFO(T1986_i0, 1);
	GET_FIFO(T1986_i1, 3);
	Butterfly(T1986_i0, T1986_i1, &T1986_o0, &T1986_o1, T1986_W);
	PUT_FIFO(T1986_o0, 2);
	PUT_FIFO(T1986_o1, 3);

	GET_FIFO(T1987_i0, 1);
	GET_FIFO(T1987_i1, 3);
	Butterfly(T1987_i0, T1987_i1, &T1987_o0, &T1987_o1, T1987_W);
	PUT_FIFO(T1987_o0, 2);
	PUT_FIFO(T1987_o1, 3);

	GET_FIFO(T1988_i0, 1);
	GET_FIFO(T1988_i1, 3);
	Butterfly(T1988_i0, T1988_i1, &T1988_o0, &T1988_o1, T1988_W);
	PUT_FIFO(T1988_o0, 2);
	PUT_FIFO(T1988_o1, 3);

	GET_FIFO(T1989_i0, 1);
	GET_FIFO(T1989_i1, 3);
	Butterfly(T1989_i0, T1989_i1, &T1989_o0, &T1989_o1, T1989_W);
	PUT_FIFO(T1989_o0, 2);
	PUT_FIFO(T1989_o1, 3);

	GET_FIFO(T1990_i0, 1);
	GET_FIFO(T1990_i1, 3);
	Butterfly(T1990_i0, T1990_i1, &T1990_o0, &T1990_o1, T1990_W);
	PUT_FIFO(T1990_o0, 2);
	PUT_FIFO(T1990_o1, 3);

	GET_FIFO(T1991_i0, 1);
	GET_FIFO(T1991_i1, 3);
	Butterfly(T1991_i0, T1991_i1, &T1991_o0, &T1991_o1, T1991_W);
	PUT_FIFO(T1991_o0, 2);
	PUT_FIFO(T1991_o1, 3);

	GET_FIFO(T1992_i0, 1);
	GET_FIFO(T1992_i1, 3);
	Butterfly(T1992_i0, T1992_i1, &T1992_o0, &T1992_o1, T1992_W);
	PUT_FIFO(T1992_o0, 2);
	PUT_FIFO(T1992_o1, 3);

	GET_FIFO(T1993_i0, 1);
	GET_FIFO(T1993_i1, 3);
	Butterfly(T1993_i0, T1993_i1, &T1993_o0, &T1993_o1, T1993_W);
	PUT_FIFO(T1993_o0, 2);
	PUT_FIFO(T1993_o1, 3);

	GET_FIFO(T1994_i0, 1);
	GET_FIFO(T1994_i1, 3);
	Butterfly(T1994_i0, T1994_i1, &T1994_o0, &T1994_o1, T1994_W);
	PUT_FIFO(T1994_o0, 2);
	PUT_FIFO(T1994_o1, 3);

	GET_FIFO(T1995_i0, 1);
	GET_FIFO(T1995_i1, 3);
	Butterfly(T1995_i0, T1995_i1, &T1995_o0, &T1995_o1, T1995_W);
	PUT_FIFO(T1995_o0, 2);
	PUT_FIFO(T1995_o1, 3);

	GET_FIFO(T1996_i0, 1);
	GET_FIFO(T1996_i1, 3);
	Butterfly(T1996_i0, T1996_i1, &T1996_o0, &T1996_o1, T1996_W);
	PUT_FIFO(T1996_o0, 2);
	PUT_FIFO(T1996_o1, 3);

	GET_FIFO(T1997_i0, 1);
	GET_FIFO(T1997_i1, 3);
	Butterfly(T1997_i0, T1997_i1, &T1997_o0, &T1997_o1, T1997_W);
	PUT_FIFO(T1997_o0, 2);
	PUT_FIFO(T1997_o1, 3);

	GET_FIFO(T1998_i0, 1);
	GET_FIFO(T1998_i1, 3);
	Butterfly(T1998_i0, T1998_i1, &T1998_o0, &T1998_o1, T1998_W);
	PUT_FIFO(T1998_o0, 2);
	PUT_FIFO(T1998_o1, 3);

	GET_FIFO(T1999_i0, 1);
	GET_FIFO(T1999_i1, 3);
	Butterfly(T1999_i0, T1999_i1, &T1999_o0, &T1999_o1, T1999_W);
	PUT_FIFO(T1999_o0, 2);
	PUT_FIFO(T1999_o1, 3);

	GET_FIFO(T2000_i0, 1);
	GET_FIFO(T2000_i1, 3);
	Butterfly(T2000_i0, T2000_i1, &T2000_o0, &T2000_o1, T2000_W);
	PUT_FIFO(T2000_o0, 2);
	PUT_FIFO(T2000_o1, 3);

	GET_FIFO(T2001_i0, 1);
	GET_FIFO(T2001_i1, 3);
	Butterfly(T2001_i0, T2001_i1, &T2001_o0, &T2001_o1, T2001_W);
	PUT_FIFO(T2001_o0, 2);
	PUT_FIFO(T2001_o1, 3);

	GET_FIFO(T2002_i0, 1);
	GET_FIFO(T2002_i1, 3);
	Butterfly(T2002_i0, T2002_i1, &T2002_o0, &T2002_o1, T2002_W);
	PUT_FIFO(T2002_o0, 2);
	PUT_FIFO(T2002_o1, 3);

	GET_FIFO(T2003_i0, 1);
	GET_FIFO(T2003_i1, 3);
	Butterfly(T2003_i0, T2003_i1, &T2003_o0, &T2003_o1, T2003_W);
	PUT_FIFO(T2003_o0, 2);
	PUT_FIFO(T2003_o1, 3);

	GET_FIFO(T2004_i0, 1);
	GET_FIFO(T2004_i1, 3);
	Butterfly(T2004_i0, T2004_i1, &T2004_o0, &T2004_o1, T2004_W);
	PUT_FIFO(T2004_o0, 2);
	PUT_FIFO(T2004_o1, 3);

	GET_FIFO(T2005_i0, 1);
	GET_FIFO(T2005_i1, 3);
	Butterfly(T2005_i0, T2005_i1, &T2005_o0, &T2005_o1, T2005_W);
	PUT_FIFO(T2005_o0, 2);
	PUT_FIFO(T2005_o1, 3);

	GET_FIFO(T2006_i0, 1);
	GET_FIFO(T2006_i1, 3);
	Butterfly(T2006_i0, T2006_i1, &T2006_o0, &T2006_o1, T2006_W);
	PUT_FIFO(T2006_o0, 2);
	PUT_FIFO(T2006_o1, 3);

	GET_FIFO(T2007_i0, 1);
	GET_FIFO(T2007_i1, 3);
	Butterfly(T2007_i0, T2007_i1, &T2007_o0, &T2007_o1, T2007_W);
	PUT_FIFO(T2007_o0, 2);
	PUT_FIFO(T2007_o1, 3);

	GET_FIFO(T2008_i0, 1);
	GET_FIFO(T2008_i1, 3);
	Butterfly(T2008_i0, T2008_i1, &T2008_o0, &T2008_o1, T2008_W);
	PUT_FIFO(T2008_o0, 2);
	PUT_FIFO(T2008_o1, 3);

	GET_FIFO(T2009_i0, 1);
	GET_FIFO(T2009_i1, 3);
	Butterfly(T2009_i0, T2009_i1, &T2009_o0, &T2009_o1, T2009_W);
	PUT_FIFO(T2009_o0, 2);
	PUT_FIFO(T2009_o1, 3);

	GET_FIFO(T2010_i0, 1);
	GET_FIFO(T2010_i1, 3);
	Butterfly(T2010_i0, T2010_i1, &T2010_o0, &T2010_o1, T2010_W);
	PUT_FIFO(T2010_o0, 2);
	PUT_FIFO(T2010_o1, 3);

	GET_FIFO(T2011_i0, 1);
	GET_FIFO(T2011_i1, 3);
	Butterfly(T2011_i0, T2011_i1, &T2011_o0, &T2011_o1, T2011_W);
	PUT_FIFO(T2011_o0, 2);
	PUT_FIFO(T2011_o1, 3);

	GET_FIFO(T2012_i0, 1);
	GET_FIFO(T2012_i1, 3);
	Butterfly(T2012_i0, T2012_i1, &T2012_o0, &T2012_o1, T2012_W);
	PUT_FIFO(T2012_o0, 2);
	PUT_FIFO(T2012_o1, 3);

	GET_FIFO(T2013_i0, 1);
	GET_FIFO(T2013_i1, 3);
	Butterfly(T2013_i0, T2013_i1, &T2013_o0, &T2013_o1, T2013_W);
	PUT_FIFO(T2013_o0, 2);
	PUT_FIFO(T2013_o1, 3);

	GET_FIFO(T2014_i0, 1);
	GET_FIFO(T2014_i1, 3);
	Butterfly(T2014_i0, T2014_i1, &T2014_o0, &T2014_o1, T2014_W);
	PUT_FIFO(T2014_o0, 2);
	PUT_FIFO(T2014_o1, 3);

	GET_FIFO(T2015_i0, 1);
	GET_FIFO(T2015_i1, 3);
	Butterfly(T2015_i0, T2015_i1, &T2015_o0, &T2015_o1, T2015_W);
	PUT_FIFO(T2015_o0, 2);
	PUT_FIFO(T2015_o1, 3);

	GET_FIFO(T2016_i0, 1);
	GET_FIFO(T2016_i1, 3);
	Butterfly(T2016_i0, T2016_i1, &T2016_o0, &T2016_o1, T2016_W);
	PUT_FIFO(T2016_o0, 2);
	PUT_FIFO(T2016_o1, 3);

	GET_FIFO(T2017_i0, 1);
	GET_FIFO(T2017_i1, 3);
	Butterfly(T2017_i0, T2017_i1, &T2017_o0, &T2017_o1, T2017_W);
	PUT_FIFO(T2017_o0, 2);
	PUT_FIFO(T2017_o1, 3);

	GET_FIFO(T2018_i0, 1);
	GET_FIFO(T2018_i1, 3);
	Butterfly(T2018_i0, T2018_i1, &T2018_o0, &T2018_o1, T2018_W);
	PUT_FIFO(T2018_o0, 2);
	PUT_FIFO(T2018_o1, 3);

	GET_FIFO(T2019_i0, 1);
	GET_FIFO(T2019_i1, 3);
	Butterfly(T2019_i0, T2019_i1, &T2019_o0, &T2019_o1, T2019_W);
	PUT_FIFO(T2019_o0, 2);
	PUT_FIFO(T2019_o1, 3);

	GET_FIFO(T2020_i0, 1);
	GET_FIFO(T2020_i1, 3);
	Butterfly(T2020_i0, T2020_i1, &T2020_o0, &T2020_o1, T2020_W);
	PUT_FIFO(T2020_o0, 2);
	PUT_FIFO(T2020_o1, 3);

	GET_FIFO(T2021_i0, 1);
	GET_FIFO(T2021_i1, 3);
	Butterfly(T2021_i0, T2021_i1, &T2021_o0, &T2021_o1, T2021_W);
	PUT_FIFO(T2021_o0, 2);
	PUT_FIFO(T2021_o1, 3);

	GET_FIFO(T2022_i0, 1);
	GET_FIFO(T2022_i1, 3);
	Butterfly(T2022_i0, T2022_i1, &T2022_o0, &T2022_o1, T2022_W);
	PUT_FIFO(T2022_o0, 2);
	PUT_FIFO(T2022_o1, 3);

	GET_FIFO(T2023_i0, 1);
	GET_FIFO(T2023_i1, 3);
	Butterfly(T2023_i0, T2023_i1, &T2023_o0, &T2023_o1, T2023_W);
	PUT_FIFO(T2023_o0, 2);
	PUT_FIFO(T2023_o1, 3);

	GET_FIFO(T2024_i0, 1);
	GET_FIFO(T2024_i1, 3);
	Butterfly(T2024_i0, T2024_i1, &T2024_o0, &T2024_o1, T2024_W);
	PUT_FIFO(T2024_o0, 2);
	PUT_FIFO(T2024_o1, 3);

	GET_FIFO(T2025_i0, 1);
	GET_FIFO(T2025_i1, 3);
	Butterfly(T2025_i0, T2025_i1, &T2025_o0, &T2025_o1, T2025_W);
	PUT_FIFO(T2025_o0, 2);
	PUT_FIFO(T2025_o1, 3);

	GET_FIFO(T2026_i0, 1);
	GET_FIFO(T2026_i1, 3);
	Butterfly(T2026_i0, T2026_i1, &T2026_o0, &T2026_o1, T2026_W);
	PUT_FIFO(T2026_o0, 2);
	PUT_FIFO(T2026_o1, 3);

	GET_FIFO(T2027_i0, 1);
	GET_FIFO(T2027_i1, 3);
	Butterfly(T2027_i0, T2027_i1, &T2027_o0, &T2027_o1, T2027_W);
	PUT_FIFO(T2027_o0, 2);
	PUT_FIFO(T2027_o1, 3);

	GET_FIFO(T2028_i0, 1);
	GET_FIFO(T2028_i1, 3);
	Butterfly(T2028_i0, T2028_i1, &T2028_o0, &T2028_o1, T2028_W);
	PUT_FIFO(T2028_o0, 2);
	PUT_FIFO(T2028_o1, 3);

	GET_FIFO(T2029_i0, 1);
	GET_FIFO(T2029_i1, 3);
	Butterfly(T2029_i0, T2029_i1, &T2029_o0, &T2029_o1, T2029_W);
	PUT_FIFO(T2029_o0, 2);
	PUT_FIFO(T2029_o1, 3);

	GET_FIFO(T2030_i0, 1);
	GET_FIFO(T2030_i1, 3);
	Butterfly(T2030_i0, T2030_i1, &T2030_o0, &T2030_o1, T2030_W);
	PUT_FIFO(T2030_o0, 2);
	PUT_FIFO(T2030_o1, 3);

	GET_FIFO(T2031_i0, 1);
	GET_FIFO(T2031_i1, 3);
	Butterfly(T2031_i0, T2031_i1, &T2031_o0, &T2031_o1, T2031_W);
	PUT_FIFO(T2031_o0, 2);
	PUT_FIFO(T2031_o1, 3);

	GET_FIFO(T2032_i0, 1);
	GET_FIFO(T2032_i1, 3);
	Butterfly(T2032_i0, T2032_i1, &T2032_o0, &T2032_o1, T2032_W);
	PUT_FIFO(T2032_o0, 2);
	PUT_FIFO(T2032_o1, 3);

	GET_FIFO(T2033_i0, 1);
	GET_FIFO(T2033_i1, 3);
	Butterfly(T2033_i0, T2033_i1, &T2033_o0, &T2033_o1, T2033_W);
	PUT_FIFO(T2033_o0, 2);
	PUT_FIFO(T2033_o1, 3);

	GET_FIFO(T2034_i0, 1);
	GET_FIFO(T2034_i1, 3);
	Butterfly(T2034_i0, T2034_i1, &T2034_o0, &T2034_o1, T2034_W);
	PUT_FIFO(T2034_o0, 2);
	PUT_FIFO(T2034_o1, 3);

	GET_FIFO(T2035_i0, 1);
	GET_FIFO(T2035_i1, 3);
	Butterfly(T2035_i0, T2035_i1, &T2035_o0, &T2035_o1, T2035_W);
	PUT_FIFO(T2035_o0, 2);
	PUT_FIFO(T2035_o1, 3);

	GET_FIFO(T2036_i0, 1);
	GET_FIFO(T2036_i1, 3);
	Butterfly(T2036_i0, T2036_i1, &T2036_o0, &T2036_o1, T2036_W);
	PUT_FIFO(T2036_o0, 2);
	PUT_FIFO(T2036_o1, 3);

	GET_FIFO(T2037_i0, 1);
	GET_FIFO(T2037_i1, 3);
	Butterfly(T2037_i0, T2037_i1, &T2037_o0, &T2037_o1, T2037_W);
	PUT_FIFO(T2037_o0, 2);
	PUT_FIFO(T2037_o1, 3);

	GET_FIFO(T2038_i0, 1);
	GET_FIFO(T2038_i1, 3);
	Butterfly(T2038_i0, T2038_i1, &T2038_o0, &T2038_o1, T2038_W);
	PUT_FIFO(T2038_o0, 2);
	PUT_FIFO(T2038_o1, 3);

	GET_FIFO(T2039_i0, 1);
	GET_FIFO(T2039_i1, 3);
	Butterfly(T2039_i0, T2039_i1, &T2039_o0, &T2039_o1, T2039_W);
	PUT_FIFO(T2039_o0, 2);
	PUT_FIFO(T2039_o1, 3);

	GET_FIFO(T2040_i0, 1);
	GET_FIFO(T2040_i1, 3);
	Butterfly(T2040_i0, T2040_i1, &T2040_o0, &T2040_o1, T2040_W);
	PUT_FIFO(T2040_o0, 2);
	PUT_FIFO(T2040_o1, 3);

	GET_FIFO(T2041_i0, 1);
	GET_FIFO(T2041_i1, 3);
	Butterfly(T2041_i0, T2041_i1, &T2041_o0, &T2041_o1, T2041_W);
	PUT_FIFO(T2041_o0, 2);
	PUT_FIFO(T2041_o1, 3);

	GET_FIFO(T2042_i0, 1);
	GET_FIFO(T2042_i1, 3);
	Butterfly(T2042_i0, T2042_i1, &T2042_o0, &T2042_o1, T2042_W);
	PUT_FIFO(T2042_o0, 2);
	PUT_FIFO(T2042_o1, 3);

	GET_FIFO(T2043_i0, 1);
	GET_FIFO(T2043_i1, 3);
	Butterfly(T2043_i0, T2043_i1, &T2043_o0, &T2043_o1, T2043_W);
	PUT_FIFO(T2043_o0, 2);
	PUT_FIFO(T2043_o1, 3);

	GET_FIFO(T2044_i0, 1);
	GET_FIFO(T2044_i1, 3);
	Butterfly(T2044_i0, T2044_i1, &T2044_o0, &T2044_o1, T2044_W);
	PUT_FIFO(T2044_o0, 2);
	PUT_FIFO(T2044_o1, 3);

	GET_FIFO(T2045_i0, 1);
	GET_FIFO(T2045_i1, 3);
	Butterfly(T2045_i0, T2045_i1, &T2045_o0, &T2045_o1, T2045_W);
	PUT_FIFO(T2045_o0, 2);
	PUT_FIFO(T2045_o1, 3);

	GET_FIFO(T2046_i0, 1);
	GET_FIFO(T2046_i1, 3);
	Butterfly(T2046_i0, T2046_i1, &T2046_o0, &T2046_o1, T2046_W);
	PUT_FIFO(T2046_o0, 2);
	PUT_FIFO(T2046_o1, 3);

	GET_FIFO(T2047_i0, 1);
	GET_FIFO(T2047_i1, 3);
	Butterfly(T2047_i0, T2047_i1, &T2047_o0, &T2047_o1, T2047_W);
	PUT_FIFO(T2047_o0, 2);
	PUT_FIFO(T2047_o1, 3);
}
