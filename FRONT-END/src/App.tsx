import { useState, useCallback } from 'react'

type CellType = 0 | 1 | 2 | 3 | 4
type Method = 'BFS' | 'DFS' | 'PROF_LIMITADA' | 'APROF_ITERATIVO' | 'BIDIRECIONAL' | 'CUSTO_UNIFORME' | 'GREEDY' | 'ASTAR' | 'AIA_ESTRELA'

const GRID_SIZE = 10

const CELL_COLORS: Record<CellType, string> = {
  0: 'bg-white',
  1: 'bg-black',
  2: 'bg-green-500',
  3: 'bg-red-500',
  4: 'bg-blue-500',
}

const CELL_LABELS: Record<CellType, string> = {
  0: '',
  1: '',
  2: 'Início',
  3: 'Fim',
  4: 'Caminho',
}

function createEmptyGrid(): CellType[][] {
  return Array.from({ length: GRID_SIZE }, () =>
    Array.from({ length: GRID_SIZE }, () => 0 as CellType)
  )
}

export default function App() {
  const [grid, setGrid] = useState<CellType[][]>(createEmptyGrid)
  const [origin, setOrigin] = useState<string>('0,0')
  const [destination, setDestination] = useState<string>('9,9')
  const [method, setMethod] = useState<Method>('BFS')
  const [path, setPath] = useState<string>('')
  const [isLoading, setIsLoading] = useState(false)

  const handleCellClick = useCallback((row: number, col: number) => {
    setGrid((prev) => {
      const newGrid = prev.map((r) => [...r])
      const current = newGrid[row][col]
      if (current === 0) {
        newGrid[row][col] = 1
      } else if (current === 1) {
        newGrid[row][col] = 0
      }
      return newGrid
    })
  }, [])

  const handleResetGrid = useCallback(() => {
    setGrid(createEmptyGrid())
    setPath('')
  }, [])

  const handleExecutar = async () => {
    setIsLoading(true)
    try {
      const response = await fetch('http://localhost:8000/resolver', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          origem: origin,
          destino: destination,
          metodo: method,
          grid: grid,
        }),
      })

      if (!response.ok) {
        throw new Error(`Erro na requisição: ${response.status}`)
      }

      const data = await response.json()

      if (data.caminho) {
        setPath(data.caminho)
      }

      if (data.grid) {
        setGrid(data.grid)
      }
    } catch (error) {
      console.error('Erro ao resolver o labirinto:', error)
      setPath('Erro ao conectar ao servidor. Certifique-se de que o backend está a correr em localhost:8000.')
    } finally {
      setIsLoading(false)
    }
  }

  const cellSize = 'w-8 h-8 sm:w-10 sm:h-10 md:w-12 md:h-12 lg:w-14 lg:h-14'

  return (
    <div className="flex h-screen w-screen overflow-hidden bg-gray-50">
      {/* Barra Lateral Esquerda - Painel de Controlo */}
      <aside className="flex w-[30%] min-w-[280px] flex-col gap-5 overflow-y-auto bg-gray-100 p-6 shadow-xl">
        <h1 className="text-xl font-bold text-gray-800">Configuração do Labirinto</h1>

        <div className="flex flex-col gap-2">
          <label htmlFor="origin" className="text-sm font-semibold text-gray-700">
            Origem (X,Y)
          </label>
          <input
            id="origin"
            type="text"
            value={origin}
            onChange={(e) => setOrigin(e.target.value)}
            placeholder="Ex: 0,0"
            className="rounded-lg border border-gray-300 px-3 py-2 text-sm outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-200"
          />
        </div>

        <div className="flex flex-col gap-2">
          <label htmlFor="destination" className="text-sm font-semibold text-gray-700">
            Destino (X,Y)
          </label>
          <input
            id="destination"
            type="text"
            value={destination}
            onChange={(e) => setDestination(e.target.value)}
            placeholder="Ex: 9,9"
            className="rounded-lg border border-gray-300 px-3 py-2 text-sm outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-200"
          />
        </div>

        <div className="flex flex-col gap-2">
          <label htmlFor="method" className="text-sm font-semibold text-gray-700">
            Método
          </label>
          <select
            id="method"
            value={method}
            onChange={(e) => setMethod(e.target.value as Method)}
            className="rounded-lg border border-gray-300 bg-white px-3 py-2 text-sm outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-200"
          >
            <option value="BFS">Busca em Largura (BFS)</option>
            <option value="DFS">Busca em Profundidade (DFS)</option>
            <option value="PROF_LIMITADA">Profundidade Limitada</option>
            <option value="APROF_ITERATIVO">Aprofundamento Iterativo</option>
            <option value="BIDIRECIONAL">Busca Bidirecional</option>
            <option value="CUSTO_UNIFORME">Custo Uniforme</option>
            <option value="GREEDY">Greedy</option>
            <option value="ASTAR">A* (A-Star)</option>
            <option value="AIA_ESTRELA">AIA-Estrela</option>
          </select>
        </div>

        <button
          onClick={handleExecutar}
          disabled={isLoading}
          className="mt-1 rounded-lg bg-blue-600 py-2.5 text-sm font-semibold text-white shadow-md transition hover:bg-blue-700 active:scale-[0.98] disabled:cursor-not-allowed disabled:opacity-60"
        >
          {isLoading ? 'A executar...' : 'Executar'}
        </button>

        <button
          onClick={handleResetGrid}
          className="rounded-lg border border-gray-300 bg-white py-2 text-sm font-semibold text-gray-600 shadow-sm transition hover:bg-gray-50 active:scale-[0.98]"
        >
          Reiniciar Grid
        </button>

        <div className="flex flex-col gap-2">
          <label className="text-sm font-semibold text-gray-700">Caminho</label>
          <div className="min-h-[100px] max-h-[300px] overflow-y-auto rounded-lg border border-gray-300 bg-white p-3 text-sm text-gray-700 shadow-inner">
            {path || 'Aguardando execução...'}
          </div>
        </div>

        <div className="mt-auto flex flex-wrap gap-3 text-xs text-gray-500">
          <span className="flex items-center gap-1">
            <span className="inline-block h-3 w-3 rounded-sm border border-gray-300 bg-white" /> Livre
          </span>
          <span className="flex items-center gap-1">
            <span className="inline-block h-3 w-3 rounded-sm bg-black" /> Parede
          </span>
          <span className="flex items-center gap-1">
            <span className="inline-block h-3 w-3 rounded-sm bg-green-500" /> Origem
          </span>
          <span className="flex items-center gap-1">
            <span className="inline-block h-3 w-3 rounded-sm bg-red-500" /> Destino
          </span>
          <span className="flex items-center gap-1">
            <span className="inline-block h-3 w-3 rounded-sm bg-blue-500" /> Caminho
          </span>
        </div>
      </aside>

      {/* Área Principal - O Labirinto */}
      <main className="flex flex-1 items-center justify-center p-6">
        <div className="flex flex-col items-center gap-4">
          <h2 className="text-lg font-semibold text-gray-700">Labirinto 10×10</h2>
          <p className="text-xs text-gray-400">Clique nas células para alternar entre livre e parede</p>
          <div
            className="inline-grid gap-0"
            style={{ gridTemplateColumns: `repeat(${GRID_SIZE}, 1fr)` }}
          >
            {grid.map((row, rowIndex) =>
              row.map((cell, colIndex) => (
                <div
                  key={`${rowIndex}-${colIndex}`}
                  onClick={() => handleCellClick(rowIndex, colIndex)}
                  className={`${cellSize} ${CELL_COLORS[cell]} cursor-pointer border border-gray-300 transition hover:opacity-80 flex items-center justify-center text-[10px] font-bold text-white/90 select-none`}
                  title={CELL_LABELS[cell] || `Linha ${rowIndex}, Col ${colIndex}`}
                >
                  {cell !== 0 && cell !== 1 ? CELL_LABELS[cell] : ''}
                </div>
              ))
            )}
          </div>
        </div>
      </main>
    </div>
  )
}