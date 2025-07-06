import Image from "next/image";

export default function Demo() {
  return (
    <section id="demo" className="py-16 sm:py-24 bg-secondary dark:from-gray-900 dark:to-blue-900/20">
      <div className="container mx-auto px-4">
        <div className="mx-auto max-w-4xl">
          <div className="relative overflow-hidden rounded-2xl border-4 border-black/80 dark:border-gray-800 shadow-2xl shadow-blue-500/20 dark:shadow-blue-500/10 transform transition-transform duration-500 hover:scale-[1.02]">
            <div className="absolute inset-0 bg-gradient-to-r from-blue-500/10 to-purple-500/10 dark:from-blue-700/10 dark:to-purple-700/10"></div>
            <div className="relative bg-black dark:bg-gray-800">
              <div className="flex justify-center items-center p-2 bg-gradient-to-r from-blue-600 to-purple-600">
                <div className="flex space-x-1.5">
                  <div className="w-3 h-3 rounded-full bg-red-400"></div>
                  <div className="w-3 h-3 rounded-full bg-yellow-400"></div>
                  <div className="w-3 h-3 rounded-full bg-green-400"></div>
                </div>
              </div>
              <Image
                src="https://raw.githubusercontent.com/sandip-pathe/projects/refs/heads/main/demo.png"
                alt="Arin App Demo"
                width={1366}
                height={694}
                className="w-full h-auto object-contain"
                data-ai-hint="app interface"
              />
            </div>
          </div>
          <div className="mt-8 flex justify-center">
            <div className="inline-flex items-center space-x-2 px-4 py-2 bg-white rounded-full shadow-md">
              <div className="h-3 w-3 rounded-full bg-red-200 animate-pulse"></div>
              <span className="text-sm font-medium text-foreground dark:text-gray-300">
                Live Demo
              </span>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}