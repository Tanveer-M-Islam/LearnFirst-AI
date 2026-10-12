import type { Metadata } from 'next';
import './globals.css';
export const metadata: Metadata = {title:'LearnFirst AI — Think first. Learn better.',description:'An adaptive learning demo that turns small hints into independent understanding.',icons:{icon:'/favicon.svg'}};
export default function RootLayout({children}:Readonly<{children:React.ReactNode}>){return <html lang="en"><body>{children}</body></html>;}
